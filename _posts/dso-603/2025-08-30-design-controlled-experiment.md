---
layout: distill
title: "Case Study: Causal Effect of ETA Reduction"
description: "A practical case study on measuring the causal effect of reducing Estimated Time of Arrival (ETA) in a ridesharing marketplace."
date: 2025-08-29
categories: dso-603 statistics
tags: causal-inference case-study marketplace experimentation
project: dso-603
authors:
  - name: Jongmin Mun
    url: "https://jong-min.org"
bibliography: 2025-08-29-eta-reduction-case-study.bib
---


# A/B Test Design Framework

The engineering team implemented a new feature. As a data scientist you are asked to design an experiment to measure the impact of the new feature. Before running the test, you shoul first report your manager about the implementation plan.

If this is an interview, you should outline the general framework first, and then dig into details. That way the interviewer can give you points for knowing all of the steps, and you don’t risk running out of time because you went into a ton of detail on the first one or two
As a candidate, it will also be your responsibility to suss out what the interviewer cares about. They might care that you have business/product sense, in which case you spend a little more time in phase 1. Or they might primarily want to make sure you have technical chops, in which case you spend more time in phase 2.

## Phase 1: Set the context for the experiment. 
Why do we want to AB test, what is our goal, what do we want to measure?

### Business Goal
The first step is to clarify the purpose and value of the experiment with the manager. Is it even worth running an A/B test? Managers want to know that the data scientist can tie experiments to business goals.

### Specify Treatment and Hypothesis

Specify what exactly is the treatment, and what hypothesis are we testing? Too often data scientists fail to specify what the treatment is, and what is the hypothesis that they want to test. It’s important to spell this out for your manager. 

### Define the metrics
After specifying the treatment and the hypothesis, you need to define the metrics that you will track and measure.

- Success metrics: Identify at least 2-3 candidate success metrics. Then narrow it down to one and propose it to the manager to get their thoughts.
- Guardrail metrics: Guardrail metrics are metrics that you do not want to harm. You don’t necessarily want to improve them, but you definitely don’t want to harm them. Come up with 2-4 of these.
- Tracking metrics: Tracking metrics help explain the movement in the success metrics. Come up with 1-4 of these.

## Phase 2: How do we design the experiment to measure what we want to measure?

### Unit of randomization

Now that you have your treatment, hypothesis, and metrics, the next step is to determine the unit of randomization for the experiment, and when each unit will enter the experiment. You should pick a unit of randomization such that you can 
1. measure success your metrics
2. avoid interference and network effects
3. consider user experience

As a simple example, let’s say you want to test a treatment that changes the color of the checkout button on an ecommerce website from blue to green. How would you randomize this? You could randomize at the user level and say that every person that visits your website will be randomized into the treatment or control group. Another way would be to randomize at the **session level**, or even at the **checkout page level**. 

When each unit will enter the experiment is also important. Using the example above, you could have a person enter the experiment as soon as they visit the website. However, many users will not get all the way to the checkout page so you will end up with a lot of users who never even got a chance to see your treatment, which will dilute your experiment. In this case, it might make sense to have a person enter the experiment once they reach the checkout page. You want to choose your unit of randomization and when they will enter the experiment such that you have minimal dilution. In a perfect world, every unit would have the chance to be exposed to your treatment.

### Statistical Tests

Next, you need to determine which statistical test(s) you will use to analyze the results. 
- Is a simple t-test sufficient, or do you need quasi-experimental techniques like difference in differences?
- Do you require heteroskedastic robust standard errors or clustered standard errors?


The t-test and z-test of proportions are two of the most common tests.

Sometimes you might need to use difference-in-difference in an AB test. This is common when doing a geography based randomization on a relatively small sample size. Let’s say that you want to randomize by city in the state of California. It’s likely that even though you are randomizing which cities are in the treatment and control groups, that your two groups will have pre-existing biases. A common solution is to use difference-in-difference. I’m not saying this is right or wrong, but it’s a common solution that I have seen in tech companies.

### Power analysis and sample size calculation
The next step is to conduct a power analysis to determine the number of observations required and how long to run the experiment. You can either state that you would conduct a power analysis using an alpha of 0.05 and power of 80%, or ask the manager if the company has standards you should use.

I’m not going to go into how to calculate power here, but know that **in any AB  test implementation plan, you will have to mention power**. For some companies, and in junior roles, just mentioning this will be good enough. Other companies, especially for more senior roles, might ask you more specifics about how to calculate power. 

If your unit of randomization is larger than your analysis unit, you may need to adjust how you calculate your standard errors.

### Further considerations

- Are you testing multiple metrics? If so, account for that in your analysis. A really common academic answer is the Bonferonni correction. I've never seen anyone use it in real life though, because it is too conservative. A more common way is to control the False Discovery Rate. The book Trustworthy Online Controlled Experiments by Ron Kohavi discusses how to do this.

- Do any stakeholders need to be informed about the experiment? 

- Are there any novelty effects or change aversion that could impact interpretation?


- Regarding experiment design, I wanted to add a point that Ideally we should keep the experiment at small traffic (1%) and perform data quality checks in the next 2 days and if there are no bugs and if the data seems fine, then ramp up the percentage. This also ensures that if there are any negative effects due to the experiment we could avoid it affecting a larger sample size.

## Phase 3: The experiment is over. Now what?

After you “run” the A/B test, you now have some data. Consider what recommendations you can make from them. What insights can you derive to take actionable steps for the business? Speaking to this will earn you brownie points with the manager.

For example, can you think of some useful ways to segment your experiment data to determine whether there were heterogeneous treatment effects?

## Common follow-up questions, or “gotchas”

These are common questions that managers will ask to see if you really understand A/B testing.

Let’s say that you are mid-way through running your A/B test and the performance starts to get worse. It had a strong start but now your success metric is degrading. Why do you think this could be?

A common answer is novelty effect

Let’s say that your AB test is concluded and your chosen p-value cutoff is 0.05. However, your success metric has a p-value of 0.06. What do you do?

Some options are: Extend the experiment. Run the experiment again.

You can also say that you would discuss the risk of a false positive with your business stakeholders. It may be that the treatment doesn’t have much downside, so the company is OK with rolling out the feature, even if there is no true improvement. However, this is a discussion that needs to be had with all relevant stakeholders and as a data scientist or product analyst, you need to help quantify the risk of rolling out a false positive treatment.

Your success metric was stat sig positive, but one of your guardrail metrics was harmed. What do you do?

Investigate the cause of the guardrail metric dropping. Once the cause is identified, work with the product manager or business stakeholders to update the treatment such that hopefully the guardrail will not be harmed, and run the experiment again.

Alternatively, see if there is a segment of the population where the guardrail metric was not harmed. Release the treatment to only this population segment.

Your success metric ended up being stat sig negative. How would you diagnose this? 

- Very good post and I think this encapsulates a good Product Analyst or DS - Product analytics interview on AB testing. One possible addition to the gotchas would be "explain p-value or CI to a stakeholder" sort of question. Stakeholders generally interpret frequentist concepts with Bayesian definitions. I have found some candidates will point this out and I surely give them a bonus point, without any further questions into Bayesian Statistics (unless the position is a "real DS" role and not for analytics).

#
I also give many interviews that cover AB testing, this is a generally really solid guide! I also tend to ask about managing pre-experimental imbalance (like, say, CUPED though I dont care about that specifically), Bayesian approaches to AB testing, and framing AB testing analysis as a regression task.

Let’s say that your AB test is concluded and your chosen p-value cutoff is 0.05. However, your success metric has a p-value of 0.06. What do you do?

If I asked this I'd hope for an answer like "who cares lol, just launch it."

Another question - the success of this experiment is a necessity for the promo doc of someone above you. How do we analyze a negative result until its positive ;)?

In real scenarios, there is always going to be fuzziness. 0.05 is an ambiguous cutoff anyway. I’d rather have someone who can consider the context and adapt to it. If rolling out the change has limited downsides, it’s fine to discuss adjusting the threshold, and perhaps discuss whether this was the correct threshold to begin with.

If you were conducting a ton of A/B tests with very similar methodologies, powers, and very clear cost functions, then a binary threshold can be justified. In reality those things are rarely clear, and they certainly don't justify anything about 0.05 precisely.

I'd probably say something about how the closeness of a p-value to the threshold has no meaning, but it might be reasonable to push the change anyway if the risk is low and potential reward high.

Yes, I like your answer better. If we think 0.05 threshold is too small then it should have been changed before the experiment and not after.

Of course we can admit that we were wrong when setting up the experiment and do it again with the new data, but we should have a good rationale to lift the threshold not just "we want to try again and see what happens".


# How do you estimate your effect size, or where do you typically get your effect size?
It’s usually predetermined by PMs or stakeholders as “the lift that would be worth the effort in continuing to implement”. Then you can use that to calculate the sample size with power.

Agree. I would frame this as "how much resources does it take to implement this feature? Oh it takes 2 engrs at 25% capacity, which is $2 million a year. So now the MDE is index to 2 million." Add in fudge factors to account for population sizes and how long investments need to pay off. 

Also consider what other initiatives are going on/how many resources you have. If other initiatives are delivering 5% lift and this initiative delivers 3% lift, you may not launch this and tie up resources.

Yep exactly what the other two folks have said, I rely on previous experiments or business stakeholders. If neither of those methods can produce a reasonable MDE, I'll just calculate what is the MDE that we can detect, given what I think the sample size will be.

I agree with others that it depends on additional context, but a helpful default MDE is 5%. Smaller than that is definitely okay (large companies like Airbnb go smaller), but if you go much higher, you're entering statistical theater territory.


#
Let’s say that your AB test is concluded and your chosen p-value cutoff is 0.05. However, your success metric has a p-value of 0.06. What do you do?

  Some options are: Extend the experiment. Run the experiment again.

Is this p-hacking?

It is. Experiment should be sufficiently powered from the start

Indeed it is. Peeking is a big no-no in AB testing under frequentist methodology. Either you trust the result, or don't. That's kind of an issue with p-values though, it lacks interpretability, but that's a different discussion.

It technically is p-hacking, but having a policy of "I'll re-run any experiment if the p-value is between 0.05 and 0.1" has very little impact on Type I errors, but significantly increases power, so it works well in practice.

If you wanted to be rigorous, you could frame it as a group sequential test with one interim analysis, but it leads to nearly the same approach.

# Bayesians
May I add that it would be very valuable to be able to reason about the value of Bayesian analysis versus the frequentist approach, especially given the business context and the fact that business people will interpret frequentist results in a Bayesian way anyway. Will be very relevant to be able to reason the pros and cons and consider the possibility to be using priors at all (ie experiments on logged in users)

I completely agree that knowledge of Bayesian could be useful. That said, my advice is targeted towards analytics roles at large tech companies. In my experience, this type of role is not expected to know Bayesian. I'm not saying not to learn this, but for the purpose of convincing the interviewer you know how to design AB tests, it might be better to spend time learning about the aspects I laid out in my framework


I disagree in an interview context. 

Unless the role is explicitly screening for Bayesian methods, the bigger context is generally about to how to design an industry standard test well, then how to communicate it to stakeholders ans make decisions in ambiguous situations (e.g. metric A goes up/metric B goes down, p value was 0.052). 

The other issue is that a Bayesian method is difficult to evaluate for a skilled candidate; infact the interviewer may not even be trained to evaluate a detailed Bayesian answer.  Most importantly, I think, is that these scenarios are somewhat contrived and so the discussions are all hypothetical - you can't showcase actual experience. You need a lot of domain knowledge to know what kind of priors and how to mathematically formulate it, so discussing it in these contexts end up being very theory heavy. Think about the difference in "tell me about a time you had a difficult teammate and how you resolved it" vs. "tell me what you would do in this scenario".

IMO, this is a trap for junior candidates who focus on tech methods and not soft skills. you've already been evaluated on signal for technical knowledge, dont over invest your time here. Check the box on this technical skill, then level up with your soft skills. 

# Sample ratio mismatch
Good summary thanks that!

I would perhaps touch upon SRM before going into phase 3. I see a lot of analyst not checking it beforehand, which makes the conclusions invalid.

Do you think during those interviews, advantages / disadvantages of Bayesian methods would be mentione? Also curious if (group) sequential would be mentioned.

SRM is 
Basilicy an unbalanced sampling, making your conclusion iffy at best.

Mostly tested using a chi squared and if it’s below a threshold you need to check the randomization / split for bugs.
---
Yes, SRM is super important! I ask about that when I interview data scientists for A/B testing roles.

I don't put too much weight into understanding Bayesian approaches. I love the Bayesian framework, but nearly all Bayesian A/B test calculators are useless because of bad priors. In my experience, the only candidates who understand these issues have had PhDs specializing in Bayesian stats, so I don't expect candidates to understand these issues. I just keep things frequentist in interviews.

---
Totally valid. This is meant to be a guide for convincing interviewers that you know what you're talking about regarding AB testing. Luckily, the interviewer has limited time to grill the candidate so I chose to put down the information I think is most commonly asked.

In my experience, I haven't been asked, and I also haven't asked candidates, about SRM, Bayesian methods, or sequential testing. So my response would be no. The caveat is that my advice mainly applies to product analyst type roles at tech companies. If the interview is for like a research scientist type role then I think it would be worth knowing about these more advanced topics that you mentioned.


# Large scale experiments
If you're doing a test on a large dataset (say, thousands of users or more), how important do these statistical measures become?

My understanding about many of these statistical tests is that they were designed with small datasets in mind, where there is a good chance that A could appear better than B just by chance, and not because A is actually better than B.

With large datasets, surely the difference between A and B has to be pretty small before the question of which is better is no longer obvious. And if say, A is the established system and B is the new system you're trialing out, that means switching to B will have a cost associated with it that may be hard to justify if the difference between the two is so small.
---
I would encourage you to read eg Ron Kohavi's blog posts/articles accessible from https://exp-platform.com/ ( and book mentioned by OP).

basically you do a ab test on 1000's of users but apply it to millions of users.

Google’s famous “41 shades of blue” experiment is a classic example of an OCE that translated into a $200 million (USD) increase in annual revenue (Hern Citation2014);

https://www.theguardian.com/technology/2014/feb/05/why-google-engineers-designers

"We ran '1%' experiments, showing 1% of users one blue, and another experiment showing 1% another blue. And actually, to make sure we covered all our bases, we ran forty other experiments showing all the shades of blue you could possibly imagine.

"And we saw which shades of blue people liked the most, demonstrated by how much they clicked on them. As a result we learned that a slightly purpler shade of blue was more conducive to clicking than a slightly greener shade of blue, and gee whizz, we made a decision.

"But the implications of that for us, given the scale of our business, was that we made an extra $200m a year in ad revenue."
---
I do experiments with millions of users entering into experiments and these techniques are still really important. Due to real distributions being really, really unimaginably skew for a lot of metrics, we actually get pre-experimental bias, massive outliers, and non-significance all the time.
---
What do you do when you have pre-exp bias?


When the T/C split that’s realized during the experiment was imbalanced on a metric of interest prior to the experiment.

Oh, yeah I know what pre-exp bias is. I meant what do you do when you realize you have pre-exp bias?

oh ha, my bad. We basically just add a covariate which is the pre-experiment value of the metric. So if we're looking at sales, and the experiment runs 30 days, we add a covariate which is prior 30 day sales.



Gotcha. I use that technique as well when I encounter pre-exp bias.


It's important to distinguish between random and non-random pre-experiment imbalance. Random imbalance is expected and is mitigated by regression adjustment or CUPED (like you describe).

Non-random imbalance points to a randomization or data quality issue. In those situations, it's better to investigate the root cause. Non-random biased assignment with a post-hoc regression adjustment band-aid is not as trustworthy as a properly randomized experiment.

Yeah this is true. We (in principle lol) put a lot of effort into ensuring that a user doesn't enter into the experiment at the wrong time. There have been some high profile mistakes due to misidentifying when a user should enter.

100%! I've seen folks try to "data science" their way out of pre-experiment bias, when the solution was just fixing a typo with the experiment start date. It's good to check the lift vs. time graph as a first step even though it can be quite noisy.


# Case study
Question: You work for xyz company and their sign up flow has a page dedicated to membership upsell. Your team ran a test to remove that page with the aim of improving signup rates. The AB test does show a lift in sign up rate however number of memberships is Non Stat Sig. How would you validate that there is truly no impact on memberships after removing the upsell from signup flow?
# References
- [A guide to passing the A/B test interview question in tech companies](https://www.reddit.com/r/datascience/comments/1fyrawz/a_guide_to_passing_the_ab_test_interview_question/)