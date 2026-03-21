---
layout: distill
title: "Computing CDF by trapezoidal rule"
description: "A numerical integration approach to calculating the Cumulative Distribution Function directly from the Probability Density Function."
tags: python statistics integration math
categories: sta-6172
date: 2026-03-21
featured: false
project: sta-6172
authors:
  - name: Jongmin Mun
    url: "https://jongminmoon.github.io"
---

While libraries like `scipy.stats.norm.cdf` provide this right out of the box, calculating it directly serves as an excellent exercise in numerical integration.

 
The Normal **PDF** is defined mathematically as:

$$ f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2} $$

The Normal **CDF** is simply the definite integral (the area under the curve) of the PDF from $-\infty$ to our target value $x$:

$$ F(x) = \int_{-\infty}^{x} f(t) \, dt $$
 


#   Numerical Approximation (Trapezoidal Rule)
 

- If we don't use external numerical libraries like `numpy` or `scipy`, we can manually implement the Trapezoidal Rule step-by-step using only Python's built-in `math` library.
- This involves splitting the area under the curve into tiny trapezoids and summing their areas.
- Integration range: integration should start from $-\infty$ to $x$. Since we can't integrate from $-\infty$, we can use a negative number with large absolute value as a proxy. For example, $-10 \times \sigma$.
- area of trapezoid: width $\times$ average height. 
    - Width = `dx` = `(x - lower bound) / num_points`.
    - Average height = `(f(x1) + f(x2)) / 2`.
```python
import math

class Solution:
    def normal_pdf(self, x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
        """The Probability Density Function (PDF)."""
        return (1.0 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma)**2)

    def normal_cdf(self, x: float, mu: float = 0.0, sigma: float = 1.0, num_points: int = 10000) -> float:
        """The Cumulative Distribution Function (CDF) using manual Trapezoidal approximation."""
        if x >0:
            lower_bound = 0
        else:
            lower_bound = mu - 10 * sigma
        
        # If the target x is strictly lower than our integration boundary, CDF is functionally 0
        if x <= lower_bound:
            return 0.0
            
        dx = (x - lower_bound) / num_points
        total_area = 0.0
        
        # Sum the area of the trapezoidal slices
        for i in range(num_points):
            x1 = lower_bound + i * dx
            x2 = lower_bound + (i + 1) * dx
            
            y1 = self.normal_pdf(x1, mu, sigma)
            y2 = self.normal_pdf(x2, mu, sigma)
            
            # Area of trapezoid: width * average height
            total_area += dx * (y1 + y2) / 2.0
            
        return total_area

# Example usage:
sol = Solution()
print(f"CDF at x=0 via numerical approximation: {sol.normal_cdf(0)}")  # ~0.5
```

# Improve: symmetry of normal distribution
- if $x>0$, F(x) = 0.5 + $\int_{0}^{x} f(t) dt$.
- if $x<0$, F(x) = 0.5 - $\int_{x}^{0} f(t) dt = 0.5 - \int_{0}^{|x|} f(t) dt$.
- Thus we add a condition to check if x>0 and only integrate from 0 to x.

```python
import math

class Solution:
    def normal_pdf(self, x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
        """The Probability Density Function (PDF)."""
        return (1.0 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma)**2)

    def normal_cdf(self, x: float, mu: float = 0.0, sigma: float = 1.0, num_points: int = 10000) -> float:
        """The Cumulative Distribution Function (CDF) using manual Trapezoidal approximation."""

            
        dx = np.abs(x) / num_points
        total_area = 0.0
        
        # Sum the area of the trapezoidal slices
        for i in range(num_points):
            x1 = i * dx
            x2 = (i + 1) * dx
            
            y1 = self.normal_pdf(x1, mu, sigma)
            y2 = self.normal_pdf(x2, mu, sigma)
            
            # Area of trapezoid: width * average height
            total_area += dx * (y1 + y2) / 2.0
        if x > 0:
            return 0.5 + total_area
        else:
            return 0.5 - total_area


```