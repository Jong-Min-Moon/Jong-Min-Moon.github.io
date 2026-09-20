# frozen_string_literal: true
require 'jekyll'
require 'pathname'
require 'date'
require 'time'

module ProjectPosts
  # Generator that scans `_projects/<project>/_posts/*.{md,markdown}`
  # and adds them into `site.posts` / `site.collections['posts']`.
  # Also ensures project landing pages (index.md) have clean URLs and handles.
  class ProjectPostsGenerator < Jekyll::Generator
    safe true
    priority :high # Run before pagination (jekyll-paginate-v2) and archives

    def generate(site)
      return unless site.collections.key?('posts')

      projects_dir = File.join(site.source, '_projects')
      return unless Dir.exist?(projects_dir)

      # 1. Discover posts within project directories
      # Matches:
      #   _projects/<project_name>/_posts/*.{md,markdown}
      #   _projects/<project_name>/posts/*.{md,markdown}
      post_patterns = [
        File.join(projects_dir, '*', '_posts', '*.{md,markdown}'),
        File.join(projects_dir, '*', 'posts', '*.{md,markdown}')
      ]

      new_post_paths = Dir.glob(post_patterns)

      new_post_paths.each do |path|
        next unless File.file?(path)

        # Infer project handle from directory structure:
        # e.g., <source>/_projects/insurance/_posts/2026-05-19-test.md => "insurance"
        rel_path = Pathname.new(path).relative_path_from(Pathname.new(projects_dir)).to_s
        project_slug = rel_path.split(File::SEPARATOR).first

        # Check if already added to posts collection to avoid duplication
        existing_doc = site.collections['posts'].docs.find { |d| d.path == path }
        unless existing_doc
          doc = Jekyll::Document.new(path, site: site, collection: site.collections['posts'])
          doc.read

          next unless doc.published?

          # Auto-assign project attribute if missing
          doc.data['project'] ||= project_slug

          # Ensure date is parsed from filename if missing in frontmatter
          if !doc.data['date'] && File.basename(path) =~ /^(\d{4}-\d{2}-\d{2})-(.*)/
            date_str = Regexp.last_match(1)
            doc.data['date'] = (Time.parse(date_str) rescue Date.parse(date_str) rescue Time.now)
          end

          # Set default layout if not present
          doc.data['layout'] ||= 'post'

          # Add to posts collection
          site.collections['posts'].docs << doc
        end
      end

      # 2. Clean up projects collection (site.projects)
      if site.collections.key?('projects')
        # Remove any post documents that Jekyll's collection reader may have picked up
        # from inside a project's posts/ or _posts/ folder
        site.collections['projects'].docs.reject! do |doc|
          rel = (Pathname.new(doc.path).relative_path_from(Pathname.new(projects_dir)).to_s rescue '')
          parts = rel.split(File::SEPARATOR)
          is_post = parts.include?('_posts') || parts.include?('posts') || (doc.data['date'] && doc.path =~ /\d{4}-\d{2}-\d{2}/)
          is_subfile = parts.length >= 2 && doc.basename_without_ext != 'index'
          is_post || is_subfile
        end

        # Normalize URL and project_handle for project index documents
        site.collections['projects'].docs.each do |doc|
          rel = (Pathname.new(doc.path).relative_path_from(Pathname.new(projects_dir)).to_s rescue '')
          parts = rel.split(File::SEPARATOR)
          if parts.length >= 2 && doc.basename_without_ext == 'index'
            project_handle = parts.first
            doc.data['permalink'] ||= "/projects/#{project_handle}/"
            doc.data['project_handle'] ||= project_handle
          elsif doc.basename_without_ext != 'index'
            # Standalone single-file project: e.g. _projects/kidney.md
            doc.data['project_handle'] ||= doc.basename_without_ext
          end
        end
      end

      # 3. Sort posts by date descending so pagination and blog listings work accurately
      site.collections['posts'].docs.sort_by! { |doc| doc.date || Time.at(0) }.reverse!
    end
  end
end
