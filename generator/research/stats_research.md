# Statistics & Probability — research for the gradientpath.site study module
**Compiled 2026-08-29. Audience: AI/ML/data engineer prepping 2026 ML / AI-engineer / product-DS loops (EU + US).**

---

## 0. What the research actually showed (read this first)

**The gating set.** Across 2026 interview guides, company question banks and practitioner writeups, the same short list gates almost every loop that has a stats round:

1. p-value / significance — and the *interpretation* follow-up, not the definition
2. Type I vs Type II, power, MDE, and "how long do we run it"
3. A/B test design end-to-end (metric → randomisation unit → sample size → decision)
4. Confidence intervals and what "95%" refers to
5. Bayes / conditional probability with a base-rate twist
6. CLT and when it does not save you (skew, dependence, small n)
7. Selection bias / sampling bias / Simpson's paradox
8. Multiple comparisons (12 metrics, 10 variants, 12 prompts — same question)
9. Bias-variance / overfitting expressed statistically
10. **New for 2026:** "your eval says 82% on 50 prompts — is that a result?"

The long tail (asked, but not gating): kurtosis, MCAR/MAR/MNAR, specific imputation methods, hypergeometric vs binomial, ANOVA mechanics, copulas, survival analysis, MCMC internals, conjugate priors. Know that they exist; do not burn prep time there.

**The structural finding.** Almost nobody is graded on the definition. `datainterview.com`'s 2026 bank is explicitly written as *"good answer / bad answer"* pairs where the bad answer is the textbook definition applied without judgement — e.g. Meta's question is not "what is a p-value" but *"lift p=0.03, CI [0.1%, 0.9%], the PM says there's a 97% chance it's positive — respond."* ([datainterview.com/blog/statistics-interview-questions](https://www.datainterview.com/blog/statistics-interview-questions))

**The 2026 shift.** The AI-engineer loop has absorbed the experimentation loop. Eval-set sizing, bootstrap CIs on eval scores, judge–human agreement, and multiplicity over prompt variants are now first-class interview content — see the 51-question LLM evals handbook ([vibeengines.com/handbook/llm-evals-interview](https://vibeengines.com/handbook/llm-evals-interview)) and `statsforevals.com`, which exists solely because "we ran 50 prompts and got 82%" became an industry-wide failure mode.

---

## 1. Numbers, formulas and rules of thumb worth memorising

| Thing | Statement | Source |
|---|---|---|
| **Sample size, quick** | `n ≈ 16σ²/δ²` **per arm**, because `2(z_{1-α/2}+z_{1-β})² = 2(1.96+0.84)² ≈ 15.7` at α=0.05, 80% power | [jong-min.org/blog/2026/sample-size](https://jong-min.org/blog/2026/sample-size/) |
| **Sample size, proportions** | `n ≈ 16·p(1-p)/δ²` per arm; for p=0.05 and δ=0.005 (10% relative) → ~304k/arm | derived from above |
| **Skewed metrics** | Kohavi's Rule 7: need at least `355 × s²` users per arm, s = skewness coefficient. Bing Revenue/User has s=17.9 → ~114k users just to reach 4.4% sensitivity | [exp-platform.com Seven Rules of Thumb](https://exp-platform.com/Documents/2014%20experimentersRulesOfThumb.pdf) |
| **Capping works** | Capping Revenue/User at Bing cut skewness **from 18 to 5.3** — a ~11× reduction in required n | same |
| **Rule of three** | 0 events in n trials → 95% upper bound on the rate ≈ `3/n`. 0 failures in 300 runs ⇒ true failure rate could still be 1% | [Rule of three (statistics)](https://en.wikipedia.org/wiki/Rule_of_three_(statistics)); [Jovanovic & Levy 1997, *Am. Statistician*](http://www.nicksun.fun/assets/misc_papers/Jovanovic_1997_A_look_at_the_rule_of_three_The_American_Statistician.pdf) |
| **Peeking cost** | Testing after every observation at nominal α=0.05 gives a real FPR of **26.1%** — >5× the advertised rate | [Evan Miller, How Not To Run an A/B Test](https://www.evanmiller.org/how-not-to-run-an-ab-test.html) |
| **Peeking cost, realistic** | Optimizely's simulations: checking every 500 visitors ⇒ ~26% FPR; every 1,000 ⇒ ~20%; continuous monitoring ⇒ 40%+. Their platform FPR went "from over 20% to under 5%" after mSPRT | [atticusli.com peeking](https://atticusli.com/replication-crisis/ab-testing-peeking-problem/); [Johari, Koomen, Pekelis & Walsh, *Peeking at A/B Tests*, KDD 2017](http://library.usc.edu.ph/ACM/KKD%202017/pdfs/p1517.pdf) |
| **Peeking correction** | To hold a true 5% with k peeks you must report at ~2.9% (1 peek), 2.2% (2), 1.0% (10) | [Evan Miller](https://www.evanmiller.org/how-not-to-run-an-ab-test.html) |
| **SRM base rate** | ~**6% of Microsoft experiments** show a sample ratio mismatch; at 10k experiments/yr that's roughly one per day | [Fabijan et al., KDD 2019](https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf) |
| **Base rate of real wins** | At Bing "perhaps **1 in 500** experiments" clears a high-ROI bar; wins that do land move key metrics **0.1%–1.0%** | [Seven Rules of Thumb](https://exp-platform.com/Documents/2014%20experimentersRulesOfThumb.pdf) |
| **Posterior on a win** | With α=0.05, β=0.20: if 1/3 of ideas are real, P(true | significant) = **89%**. If 1 in 500 are real, it collapses to **3.1%** | same |
| **Latency elasticity** | Bing: every **100 ms** speedup ⇒ **+0.6% revenue**. Amazon: 100 ms slowdown ⇒ **−1% sales**. Google: 100–400 ms ⇒ −0.2% to −0.6% searches | same |
| **Winner's curse** | Shipped-win effects shrink **20–50%** in production. Facebook News Feed (Coey & Cunningham 2019, 226 tests): shrinkage estimators cut MSE **44%** | [atticusli.com winner's curse](https://atticusli.com/replication-crisis/ab-testing-winners-curse/) |
| **Interleaving** | Netflix: ranking-quality comparisons need **>100× fewer users** than a metric A/B test for 95% power — but cannot measure retention | [Netflix TechBlog, 2017-11-29](https://netflixtechblog.com/using-interleaving-in-online-experiments-to-accelerate-algorithm-innovation-at-netflix-a04ee392ec55) |
| **Learning-effect half-life** | Google ads blindness: learning half-life ≈ **60 days**; a 90-day study captures `1−e^(−0.012·90)` ≈ **65%** of the effect | [Hohnhold et al., KDD 2015](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43887.pdf) |
| **Eval SE (Bernoulli)** | `SE = sqrt(s̄(1−s̄)/n)`. At 82% on n=50: SE = 5.4pp, 95% CI ≈ **[71%, 93%]** | [Miller, Anthropic, arXiv:2411.00640](https://arxiv.org/html/2411.00640v1) |
| **Eval SE floor** | Don't trust plain standard errors below ~**300 samples**; use Wilson intervals or a smooth bootstrap | [statsforevals.com](https://statsforevals.com/resources.html) |
| **Judge validation bar** | Judge–human agreement should meet or beat **human–human agreement**; if two humans agree 85%, an 85% judge is "another annotator" | [vibeengines.com](https://vibeengines.com/handbook/llm-evals-interview) |
| **LLM online tests** | LLM output quality is high-variance per user: often **10×–100× more users** than a UI change for the same MDE | same |
| **Sequential power cost** | Spotify simulation, n=500/arm, effect 0.2σ: GST ≈ **90%** power vs mSPRT/GAVI ≈ **72–77%** vs Bonferroni-over-14-looks ≈ 75% | [Spotify Engineering, 2023-03](https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions) |

### Formulas to be able to write on a whiteboard
```
n per arm       ≈ 16 σ² / δ²                         (α=.05, power=.80)
n per arm       = 2σ²(z_{1-α/2} + z_{1-β})² / δ²      (general)
SE of mean      = sqrt( Var(s) / n )
SE Bernoulli    = sqrt( s̄(1-s̄) / n )
SE paired diff  = sqrt( Var(s_A - s_B) / n )          ← use this to compare two models
SE clustered    = sqrt( SE²_CLT + (1/n²) Σ_c Σ_i Σ_{j≠i} (s_ic - s̄)(s_jc - s̄) )
Wilson CI       ← use instead of Wald when p near 0/1 or n small
Rule of three   0/n events → 95% upper bound ≈ 3/n
CUPED           Y_adj = Y − θ(X − E[X]),  θ = Cov(Y,X)/Var(X),  Var↓ by (1−ρ²)
Delta method    Var(X/Y) ≈ (1/μ_Y²)Var(X) − (2μ_X/μ_Y³)Cov(X,Y) + (μ_X²/μ_Y⁴)Var(Y)
Bonferroni      α' = α/m       Holm: step-down, uniformly more powerful
Benjamini–Hochberg  reject the k largest i with p_(i) ≤ (i/m)q   ← controls FDR, not FWER
```

### Named tests, when they apply, and when the standard choice is wrong

| Test | Use when | The standard choice is wrong when |
|---|---|---|
| **Two-sample z / t-test** | Comparing means, n large, roughly iid | Metric is heavy-tailed *and* n is small relative to `355s²`; or randomisation unit ≠ analysis unit (see Delta method) |
| **Welch's t-test** | Default two-sample test — unequal variances | Almost never wrong; Student's pooled t is the one that's wrong. Use Welch by default |
| **Paired t-test** | Same items scored by both systems (evals!) | Items are not truly paired, or you paired on something post-treatment |
| **Two-proportion z-test** | Conversion rates, one observation per user | Users contribute many events (need clustered SE / delta method); or p is tiny and n small (use Fisher / Wilson) |
| **Chi-square** | Independence in a contingency table; **SRM checks** | Expected cell counts < 5 (use Fisher's exact); or repeated over time without correction |
| **Fisher's exact** | Small counts, rare events | n is large — it's just slow and needlessly conservative |
| **Mann–Whitney U** | Skewed data, you care about stochastic dominance | You need to report a *mean* lift — U tests a different null; a business metric of "revenue per user" is a mean, not a rank |
| **Kolmogorov–Smirnov** | Comparing two distributions, moderate n | **Production drift monitoring at scale** — with millions of rows every trivial shift is p<0.001. Use PSI / effect size thresholds |
| **ANOVA** | 3+ groups, one factor | You then run all pairwise t-tests without correction |
| **Bootstrap (percentile / BCa)** | Any statistic with no clean SE: medians, ratios, quantiles, eval metrics | Data are dependent (bootstrap *clusters*, not rows); or you bootstrap the *selected max* without max-T correction |
| **Permutation test** | Small n, want an exact null | Units are not exchangeable (network interference) |
| **Cohen's kappa** | Two raters, categorical labels, chance-corrected | Classes are very imbalanced (kappa collapses — report per-class agreement too); >2 raters (use Fleiss'), ordinal labels (use weighted kappa), continuous (use Krippendorff's alpha or ICC) |
| **Bradley–Terry / Elo** | Pairwise win rates, arena-style rankings | Matchups are non-random or the model pool changes — see The Leaderboard Illusion |

### Sequential testing / always-valid inference / CUPED — the 2026 expected baseline

A 2026 candidate is expected to know, unprompted:

- **Fixed-horizon tests are only valid at the horizon.** Peeking without correction is the single most common production stats error.
- **Three families of fix**, and their tradeoff: **Group Sequential Tests (GST)** with Lan–DeMets alpha spending (highest power, needs a max-n estimate, batch-friendly — Spotify's choice); **Always-Valid Inference / mSPRT** (unlimited peeking, no max-n, ~15–20% power cost — Optimizely, Uber, Netflix); **GAVI** (Eppo); **corrected-alpha** (Statsig). ([Spotify Engineering](https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions), [Statsig sequential docs](https://docs.statsig.com/experiments/advanced-setup/sequential-testing))
- **"You only pay for the peeking you make"** — the alpha-spending intuition. Say this line.
- **CUPED**: regress out a pre-period covariate, `Y_adj = Y − θ(X − E[X])`. Variance drops by `1−ρ²`, so a pre-period metric correlated at ρ=0.7 removes ~50% of variance ⇒ roughly half the sample size. Requires a **pre-experiment** covariate — using an in-experiment covariate reintroduces bias. ([Deng et al., WSDM 2013](https://exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf), [Optimizely CUPED docs](https://support.optimizely.com/hc/en-us/articles/33424529987597-CUPED-Controlled-experiment-Using-Pre-Experiment-Data))
- **Variance reduction beyond CUPED**: post-stratification, control variates from ML predictions, and 2024+ work combining pre- and in-experiment data ([arXiv:2410.09027](https://arxiv.org/abs/2410.09027)).

---
# TIER 1 — FOUNDATION (probability and distributions)

---

## F1. Bayes Is a Base-Rate Machine
**Kicker:** Everyone can state Bayes' rule; the interview is really testing whether you notice the base rate is doing all the work.

- P(A|B) = P(B|A)P(A)/P(B). The interview version is a screening test: 1% prevalence, 99% sensitivity, 95% specificity → PPV ≈ 16.7%, not 99%.
- The classic factory variant: Machine A makes 60% of bulbs at a 5% defect rate, B makes 40% at 3%; given a defective bulb, P(A) = 5/7. ([Exponent](https://www.tryexponent.com/blog/top-statistics-data-science-interview-questions))
- The same structure is the whole argument for why a 95%-accurate fraud/abuse classifier at 0.1% prevalence is useless without calibration.
- Kohavi's applied version: **P(true effect | statistically significant)** depends on the prior probability that your idea works. At a 1-in-3 hit rate that posterior is 89%; at Bing's breakthrough rate of 1-in-500 it is **3.1%**.
- Say "prior odds × likelihood ratio = posterior odds" — it makes the whole family of these questions one line.

**THE FOLLOW-UP:** *"Your model flags 1,000 accounts a day at 90% precision on your test set. Fraud is 0.05% of traffic. What will the ops team actually see, and what do you change?"* (Answer: the test set was rebalanced; recompute PPV at true prevalence, then either raise threshold, add a second-stage model, or change the metric to precision@k.)

**THE TRAP:** Candidates say "accuracy 99%" and stop. Or they invert the conditional — "the test is 99% accurate so there's a 99% chance I have it" — which is the prosecutor's fallacy in a lab coat.

**REAL FAILURE:** *R v Sally Clark* (UK, 1999). Paediatrician Roy Meadow testified the chance of two cot deaths in one family was "1 in 73 million," multiplying two independent probabilities that were not independent and, crucially, never comparing it against the prior odds of double murder. Clark served three years; conviction quashed 2003; the Royal Statistical Society issued a formal protest in 2001. ([RSS statement / case summary](https://en.wikipedia.org/wiki/Sally_Clark))

---

## F2. The CLT Does Not Rescue Skewed Metrics
**Kicker:** "n > 30 so it's normal" is the single most confidently wrong sentence in stats interviews.

- CLT is about the sampling distribution of the **mean**, not the data. Convergence speed depends on skewness: the required n scales with **s²** (skewness squared).
- Kohavi's rule: you need at least **355 × s²** users per arm before the t-test's normal approximation is trustworthy. Bing's Revenue/User has s = 17.9 ⇒ ~114,000 users per arm just to detect a 4.4% change.
- Almost every money metric is heavy-tailed: revenue/user, session length, items per order, tokens per request, LLM latency.
- Fixes, in order of preference: **cap/winsorize** (Bing's capping cut skewness 18 → 5.3), switch to a bounded proxy metric, bootstrap the CI, or change the randomisation/analysis unit.
- Capping introduces bias in exchange for variance — that is a *decision*, and you must state the cap rule before you look at data.

**THE FOLLOW-UP:** *"Bookings per user is heavily right-skewed with a big spike at zero. The team wants a t-test. What do you do?"* (Airbnb's actual question — [datainterview.com](https://www.datainterview.com/blog/statistics-interview-questions))

**THE TRAP:** Reaching for Mann–Whitney "because it's non-parametric." U tests stochastic dominance, not the mean — and the business cares about total revenue, which is a mean. You have quietly changed the question.

**REAL FAILURE:** Microsoft's own experimenter rules exist because Bing teams repeatedly shipped/killed features on underpowered revenue metrics; Rule 7 ("Have Enough Users") is written as a direct correction with the 355s² table and per-metric sensitivities. ([exp-platform.com Seven Rules of Thumb, 2014](https://exp-platform.com/Documents/2014%20experimentersRulesOfThumb.pdf))

---

## F3. Independence Is the Assumption That Silently Breaks
**Kicker:** Your n is not the number of rows; it is the number of independent things you randomised.

- Variance of a sum only equals the sum of variances under independence. Every t-test, CI and p-value you compute assumes it.
- Real violations: one user generating 40 sessions; 200 eval questions drawn from 20 documents; comments nested in threads; requests nested in tenants.
- Effect: standard errors are **too small**, so p-values are too small, so you ship noise. Effective sample size falls by the design effect `1 + (m−1)ρ`.
- Fixes: cluster-robust SEs, the delta method, bootstrap **at the cluster level**, or aggregate to the randomisation unit first.
- Anthropic's eval paper gives the exact clustered-SE formula for this case because eval questions come "in related groups."

**THE FOLLOW-UP:** *"You randomised by user but you're analysing click-through-rate per impression. What's wrong and how do you fix it?"*

**THE TRAP:** "I have 2 million rows so I have tons of power." You have 40,000 users. Also: bootstrapping rows instead of clusters, which reproduces the same lie.

**REAL FAILURE:** Anthropic's *Adding Error Bars to Evals* (arXiv:2411.00640, Nov 2024) lists clustered standard errors as recommendation #2 precisely because eval suites draw multiple questions per source passage, and naive SEs understate uncertainty on published model comparisons. ([arXiv:2411.00640](https://arxiv.org/html/2411.00640v1))

---

## F4. Pick the Right Count Distribution
**Kicker:** Binomial, Poisson, negative binomial and hypergeometric are four different physical stories, and interviewers pick the one where the obvious answer is wrong.

- **Binomial**: fixed n trials, constant p, independent. **Poisson**: events in continuous time at rate λ; use λt for a window. **Hypergeometric**: sampling *without* replacement from a finite pool. **Negative binomial**: counts with overdispersion (Var > mean).
- Binomial(200, 0.02) ≈ Poisson(4) — the rare-event approximation Netflix asks about.
- Uber's version: 12 ride requests/hour, P(≥3 in 10 minutes) → Poisson with λt = 2.
- Meta's version: 5 users sampled from 100 (20 treatment, 80 control), P(exactly 2 treatment) → **hypergeometric**, not binomial.
- Google's version: *"why is Poisson wrong for click-through rate?"* — because clicks are bounded by impressions and overdispersed across users; binomial or beta-binomial fits, Poisson does not.

**THE FOLLOW-UP:** *"Your event counts have variance three times the mean. What does that tell you, and what model do you use?"* (Overdispersion → negative binomial or a mixed model; a Poisson GLM will give you SEs that are far too small.)

**THE TRAP:** Using binomial when sampling without replacement from a small pool, and using Poisson for anything that has a natural ceiling.

**REAL FAILURE / SYSTEM:** The whole question set above is documented as being asked at Meta, Uber, Netflix, Google and Spotify in 2026 loops. ([datainterview.com/blog/statistics-interview-questions](https://www.datainterview.com/blog/statistics-interview-questions))

---

## F5. Regression to the Mean Is Not a Treatment Effect
**Kicker:** If you selected a group because it was extreme, it will improve without you touching it.

- Any measurement = signal + noise. Select on a high (or low) measurement and you have selected partly on noise, which does not repeat.
- This is the mechanism behind: "our intervention for low-performing users worked," "the coaching helped the worst reps," "the model that won the hyperparameter sweep."
- It is also the mechanism behind the **winner's curse** in A/B tests (see C10) and the **decline effect** in science.
- The clean diagnostic: does the comparison group also improve? If you have no control group, you cannot distinguish the two.
- Kahneman's flight-instructor story is the canonical illustration — praise appeared to hurt and criticism to help, purely from regression.

**THE FOLLOW-UP:** *"We targeted the bottom decile of users with a re-engagement campaign and their engagement went up 12%. Ship it?"* (No — you need a randomised holdout inside that decile.)

**THE TRAP:** Claiming that "we controlled for baseline by only including low-baseline users," which is exactly the thing that creates the artefact.

**REAL FAILURE:** Genome-wide association studies. Palmer & Pe'er (PLOS Genetics 2017) showed that the winner's-curse correction *explains* replication variability in quantitative-trait GWAS — the effect sizes of the top hits are systematically inflated and shrink on replication. ([PLOS Genetics, 2017](https://journals.plos.org/plosgenetics/article?id=10.1371%2Fjournal.pgen.1006916))

---

## F6. Correlation, Causation, and the Third Thing
**Kicker:** Everyone knows the slogan; the interview tests whether you can name the specific confounder in *this* dataset within 30 seconds.

- Three explanations for any observed association: causation, reverse causation, confounding (plus selection into the sample, and pure chance).
- Practise naming them concretely: "users who use feature X retain better" → heavy users adopt more features (confound by engagement); "the notification caused the session" → users who were about to open the app got the notification (reverse causation via targeting).
- The only clean fixes are randomisation, or a design that makes the confounder irrelevant (IV, diff-in-diff, RDD).
- "I controlled for it in a regression" is only valid if you controlled for a **pre-treatment** confounder and not a mediator or collider.

**THE FOLLOW-UP:** *"You regress churn on promo exposure and find promos reduce churn. What's wrong?"* (Uber's question — promos are targeted at users predicted to churn, or at engaged users; the coefficient is a selection artefact. Propose an encouragement design or a holdout.)

**THE TRAP:** Saying "correlation is not causation" and then, two minutes later, interpreting a regression coefficient causally.

**REAL FAILURE:** Google Flu Trends. GFT fit **45 search terms selected from 50 million candidates** against 1,152 data points, and picked up winter-correlated terms (e.g. high-school basketball) rather than flu. It missed the non-seasonal 2009 H1N1 pandemic entirely and overestimated CDC ILI in **100 of 108 weeks** from August 2011, at one point predicting more than **double** the true share of doctor visits. A simple lagged-CDC autoregression beat it (MAE 0.311 vs GFT 0.486). ([Lazer et al., *Science* 343, 14 Mar 2014](https://www.science.org/doi/10.1126/science.1248506); [PDF](https://www.dhi.ac.uk/san/waysofbeing/data/data-crone-lazer-2014.pdf))

---

## F7. Expected Value, Linearity, and the Interview Brainteaser
**Kicker:** Linearity of expectation holds even when the variables are dependent — that single fact solves most of the puzzles.

- E[X+Y] = E[X] + E[Y] always; no independence needed. Var(X+Y) = Var(X)+Var(Y)+2Cov(X,Y) — independence needed there.
- Coupon-collector, indicator variables, and "expected number of X" problems all collapse under linearity.
- Law of total expectation: E[X] = E[E[X|Y]] — the tool for "expected value given a random stopping rule."
- Know the mean/variance of the standard families cold (Bernoulli p, p(1−p); Poisson λ,λ; Exponential 1/λ, 1/λ²; Uniform, Geometric).
- If you cannot derive it, **simulate it**. Saying "I'd write ten lines of NumPy to check my closed form" is a strong signal, not a weak one.

**THE FOLLOW-UP:** *"Now compute the variance."* (This is where most people fall over — they have the expectation but no covariance intuition.)

**THE TRAP:** Assuming independence to compute a variance when the problem never said so, and not flagging the assumption out loud.

**REAL SYSTEM:** Monte Carlo simulation as a first-class answer is now explicit in experimentation platform design — Airbnb built its dynamic p-value thresholds by simulating "varying values for parameters like the real effect size, variance and different levels of certainty" rather than deriving a closed form. ([Airbnb Engineering, *Experiments at Airbnb*](https://medium.com/airbnb-engineering/experiments-at-airbnb-e2db3abf39e7))

---

## F8. Long Tails Break Averages and Break Models
**Kicker:** In a long-tailed world the mean is not typical, the median is not the business metric, and your training data over-represents the head.

- Long-tail distributions show up in: purchases per customer, video watch time, query frequency, token counts, class labels in production.
- Consequences: the sample mean converges slowly, outliers dominate variance, and stratified/rare classes get almost no gradient signal.
- For classification, long-tailed labels make **accuracy** meaningless and make ROC-AUC optimistic (see A5).
- Practical handling: log/Box-Cox transforms (but you then estimate the mean of the log, not the log of the mean), capping, quantile regression, or explicitly modelling the tail.
- "Which quantile do you care about?" is often a better question than "what's the average?" — p95 latency, not mean latency.

**THE FOLLOW-UP:** *"You transformed revenue with log1p and the model looks great. How do you report the business impact?"* (You cannot exponentiate the mean of the logs and call it revenue — that's the geometric mean; use Duan's smearing estimator or model the raw scale.)

**THE TRAP:** Reporting a mean lift computed on log-transformed data as if it were a percentage lift in revenue.

**REAL FAILURE:** Long Term Capital Management, 1998. Models calibrated on normal-tailed volatility assigned near-zero probability to the joint Russian-default/flight-to-quality move; LTCM lost **$4.6 billion in under four months** and was recapitalised in a $3.6bn Fed-brokered bailout in September 1998. The direct statistical lesson: correlations and tails are not stable across regimes. ([Federal Reserve History](https://www.federalreservehistory.org/essays/ltcm-near-failure))

---

## F9. Sampling: Which Bias Are You Buying?
**Kicker:** Every dataset was collected by a process, and the process — not the size — decides what you can conclude.

- Named biases you should be able to distinguish instantly: **selection**, **survivorship**, **non-response**, **under-coverage**, **length-biased sampling**, **collider/Berkson**.
- Bigger n does not fix any of them; it just makes the CI around the wrong number narrower. This is Lazer's "big data hubris."
- Sampling designs: simple random, systematic, **stratified** (lowers variance when strata differ), **cluster** (cheaper, raises variance).
- In ML: your training set is a survey. Ask "who is missing?" before "what's my AUC?"
- Production version: your labelled data is whatever got reviewed, and what got reviewed is whatever the old model flagged.

**THE FOLLOW-UP:** *"You retrain a fraud model on the transactions your current model let through. What happens over three retraining cycles?"* (Feedback loop: the model never sees the fraud it already blocks, so its estimate of that fraud's prevalence goes to zero and it stops blocking it.)

**THE TRAP:** "We have 500 million rows, so sampling bias isn't an issue."

**REAL FAILURE:** The *Literary Digest* 1936 US presidential poll. 2.4 million responses — the largest poll ever run at the time — predicted Landon over Roosevelt 57–43. Roosevelt won 61% of the popular vote and 46 of 48 states. The sample came from telephone books and car registrations (rich, in 1936) with ~24% response. Gallup got it right with ~50,000 people. ([Wikipedia / standard reference](https://en.wikipedia.org/wiki/The_Literary_Digest#1936_opinion_poll))

---

## F10. Simulation Beats Recall
**Kicker:** The candidate who says "I'd simulate the null and look" almost always outranks the candidate who half-remembers a formula.

- Any sampling distribution can be obtained by simulation: shuffle labels for a permutation null, resample rows for a bootstrap, generate from the assumed DGP for a power analysis.
- Power analysis by simulation is strictly more general than the closed form — it handles ratio metrics, clustering, sequential rules, skew and capping in one place.
- **A/A tests** are the empirical version: run your pipeline on two random splits of control and check you get ~5% false positives. If you get 12%, your variance estimator is wrong.
- Bootstrapping the *whole pipeline* (including the metric definition) catches errors that no formula check will.
- Say the words "I'd start with an A/A test" in any experimentation design question — it is the strongest single credibility signal.

**THE FOLLOW-UP:** *"Your A/A tests come back significant 12% of the time. Name three causes."* (Clustered data analysed as iid; ratio metric with naive variance; SRM/assignment bug; a metric with an outlier problem; a peeking rule baked into the dashboard.)

**THE TRAP:** Treating A/A tests as a formality rather than a variance-estimator audit.

**REAL SYSTEM:** Twitch published simulated bootstrapped A/A tests specifically to validate their variance estimators on heavy-tailed metrics. ([Twitch Engineering, 2021-11-04](https://blog.twitch.tv/en/2021/11/04/simulated-bootstrapped-aa-tests-1/))

---
# TIER 2 — CORE (estimation and inference)

---

## C1. A p-value Is Not the Probability You Are Wrong
**Kicker:** A p-value is not the probability the null is true, not the probability you are wrong, and not the size of the effect — and the follow-up will find out whether you know that.

- Definition to say out loud: *P(data at least this extreme | null is true)*. It conditions on the null, so it cannot be a probability about the null.
- It is not 1 − P(H1). It is not the probability the result replicates. It says nothing about effect size.
- p = 0.03 with a CI of [0.1%, 0.9%] means the effect is *real and tiny*. p = 0.2 with a CI of [−1%, +9%] means *you learned nothing*.
- The ASA's 2016 statement exists because this was misused so widely; know that "statistically significant" ≠ "important."
- The probability the PM actually wants is Bayesian — P(effect > 0 | data) — and requires a prior.

**THE FOLLOW-UP (the real one, asked at Meta):** *"Your test shows a lift with p = 0.03 and a 95% CI of [0.1%, 0.9%]. The PM says 'so there's a 97% chance this is positive.' Respond."* Good answer: correct the interpretation, note the CI already tells you the effect is at most ~1%, ask whether 1% clears the launch bar, and offer a Bayesian posterior if they want a probability statement. Bad answer: accept the framing. ([datainterview.com](https://www.datainterview.com/blog/statistics-interview-questions))

**Second follow-up (near-universal):** *"The test isn't significant after two weeks. What do you do?"* The expected answer is a **decision tree, not 'run it longer'**: (1) check SRM and instrumentation first; (2) compute the observed CI — did you rule out your MDE, or is the CI so wide you're underpowered? (3) re-derive the power calc with the *observed* variance; (4) consider CUPED / a more sensitive proxy metric / interleaving; (5) if it's genuinely powered and flat, that's a real "no effect" result — ship the simpler variant.

**THE TRAP:** "p = 0.06 means it's trending toward significance." There is no such thing. Also "we failed to reject, so there is no effect" — absence of evidence.

**REAL FAILURE:** The replication crisis. The Open Science Collaboration (*Science*, Aug 2015) replicated 100 psychology studies: 97% of the originals reported p < .05, but only **36%** of replications did, and mean effect sizes **halved** (r = 0.403 → 0.197). ([*Science* 349:aac4716](https://www.science.org/doi/10.1126/science.aac4716))

---

## C2. Confidence Intervals Are About the Procedure
**Kicker:** "95% confident the true value is in this interval" is the wrong sentence, and the right sentence is more useful anyway.

- Correct: if you repeated the experiment many times, 95% of the intervals produced this way would contain the true parameter. The *procedure* has 95% coverage.
- A CI carries strictly more information than a p-value: direction, magnitude, and precision in one object.
- **Overlapping CIs do not imply a non-significant difference** — you must test the *difference*, especially for paired data.
- Width scales as 1/√n: to halve a CI you need 4× the data. This is the single most useful back-of-envelope in eval and experiment planning.
- Wald intervals fail near 0 and 1 and for small n — use **Wilson** (or Clopper-Pearson) for proportions.

**THE FOLLOW-UP:** *"Model A scores 82% and Model B scores 79% on the same 500-question eval, and their individual 95% CIs overlap. Is A better?"* (You cannot tell from overlapping marginal CIs. Compute the CI on the **paired per-question difference** — pairing removes question difficulty as a variance source and often makes a difference significant that the marginal CIs hid.)

**THE TRAP:** Two errors, both common: (a) "there's a 95% probability the true value is in [a,b]" (that's a credible interval); (b) "the CIs overlap so they're the same."

**REAL FAILURE:** *Adding Error Bars to Evals* (Miller, Anthropic, Nov 2024) exists because the industry published bare accuracy numbers with no uncertainty; its recommendation #4 is explicitly "conduct statistical inference on the question-level **paired** differences." ([arXiv:2411.00640](https://arxiv.org/html/2411.00640v1))

---

## C3. Power, MDE and the Question Behind "How Long Do We Run It?"
**Kicker:** "How long should we run the test?" is a power question wearing a project-management costume.

- Four quantities, pick three: α, power (1−β), MDE (δ), and n. Fix α = 0.05, power = 0.80, decide δ from the business, solve for n.
- `n ≈ 16σ²/δ²` per arm. For a proportion, `n ≈ 16 p(1−p)/δ²`. Halving the MDE **quadruples** the sample.
- Then convert n to days using *daily eligible users*, and round **up to whole weeks** to absorb day-of-week seasonality.
- Underpowered tests are worse than no test: they mostly produce noise, and the significant ones are heavily inflated (Type M error).
- Say "MDE" not "expected lift." The MDE is the smallest effect worth detecting, which is a product decision, not a statistical one.

**THE FOLLOW-UP:** *"Baseline conversion is 5%, you want to detect a 10% relative lift, α = 0.05, 80% power. Roughly how many users per arm and how many days?"* (δ = 0.005; n ≈ 16·0.05·0.95/0.005² ≈ 304,000 per arm; at 50k eligible users/day split two ways → ~12 days → run 14.) Being able to do this arithmetic out loud is the whole point.

**THE TRAP:** Two: (a) computing sample size from the lift you *hope* for rather than the smallest lift that matters, which guarantees underpowering; (b) forgetting that the sample size is **per arm** and that 5 variants multiplies both n and the multiplicity problem.

**REAL FAILURE:** Kohavi's Rule 2 — at Bing, wins move key metrics **0.1%–1.0%**, and "perhaps one in 500" experiments is a breakthrough. Teams that size for a 5% lift are sizing for something that essentially never happens. ([Seven Rules of Thumb](https://exp-platform.com/Documents/2014%20experimentersRulesOfThumb.pdf))

---

## C4. Peeking: The Most Expensive Free Habit
**Kicker:** Looking at the dashboard is free; *stopping* when it looks good is what costs you a 26% false positive rate.

- A fixed-horizon p-value is only valid at the fixed horizon. Repeated looks with a stop-on-significance rule inflate α, because you get many chances to cross the line.
- Evan Miller's simulation: testing after every observation at nominal 5% gives a **real FPR of 26.1%**.
- Optimizely's Monte Carlo: checking every 500 visitors → ~26%; every 1,000 → ~20%; continuous → **40%+**. After switching to mSPRT their platform FPR dropped "from over 20% to under 5%."
- To hold true 5% with k naive peeks you must report at ~2.9% (1 peek), 2.2% (2), 1.0% (10).
- The fixes: **fixed horizon + pre-registration**, **group sequential with alpha spending** (Lan–DeMets), **always-valid inference / mSPRT**, or a Bayesian decision rule with an explicit loss.

**THE FOLLOW-UP:** *"Our dashboard shows a live p-value that refreshes hourly, and the team stops when it drops below 0.05. What's wrong and how do you fix it without banning the dashboard?"* (Netflix's version of this question. Answer: keep the dashboard, change the *statistic* — serve always-valid p-values or a GST boundary so that the displayed number is valid at every look.)

**THE TRAP:** "We only peeked twice, that's basically fine." Two peeks already roughly doubles your α. Also: "we peeked but only to check for bugs" — fine *if* you never stop early on the basis of the metric, which nobody can promise.

**REAL FAILURE:** Airbnb's price-filter experiment hit p < 0.05 at day 7 showing a ~4% effect; run to completion, the effect was "practically null." Airbnb responded by building simulation-derived **time-varying p-value thresholds**. ([Airbnb Engineering, *Experiments at Airbnb*](https://medium.com/airbnb-engineering/experiments-at-airbnb-e2db3abf39e7))

---

## C5. Sequential Testing and Always-Valid Inference
**Kicker:** The 2026 expectation is not "don't peek" — it's knowing which of the three correction families you'd deploy and what it costs you.

- **Group Sequential Tests (GST)** with Lan–DeMets alpha spending: you spend α across planned looks; needs a max-n estimate; highest power; batch-friendly. Spotify's choice.
- **Always-Valid Inference / mSPRT**: unlimited peeking, no max-n needed, streaming-friendly; costs power and requires tuning a mixture variance. Optimizely, Uber, Netflix.
- **GAVI** (Eppo), **corrected-alpha** (Statsig) — same family, different knobs.
- The tradeoff with numbers (Spotify simulation, 500 obs/arm, 0.2σ effect): GST ≈ **90%** power; GAVI ≈ 72–76%; mSPRT ≈ 72–77%; Bonferroni over 14 looks ≈ 75%. Underestimating max-n by 50× cost GAVI ~30% power vs a well-configured GST.
- The soundbite: **"with alpha spending you only pay for the peeking you make."**

**THE FOLLOW-UP:** *"Why wouldn't you just always use always-valid inference, since it's strictly safer?"* (Because it's less powerful when you *can* estimate the horizon, which for a scheduled two-week test you usually can. The right answer is design-dependent, not dogmatic.)

**THE TRAP:** Naming "sequential testing" as a buzzword without being able to state the cost. Every sequential method trades power for the right to stop early; a candidate who claims it's free hasn't used it.

**REAL SYSTEM:** Spotify's public comparison of GST / mSPRT / GAVI / CAA, with power simulations, and their decision to run GST with Lan–DeMets alpha spending because their data arrives in daily batches. ([Spotify Engineering, March 2023](https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions)); Booking.com's sequential testing writeup ([booking.ai](https://booking.ai/sequential-testing-at-booking-com-650954a569c7))

---

## C6. Multiple Comparisons: 12 Metrics, 10 Variants, 12 Prompts
**Kicker:** With 20 independent tests at α = 0.05 you expect one false positive by construction, and the interviewer will hand you exactly that scenario.

- FWER with m independent tests = `1 − (1−α)^m`. m=12 → 46%. m=20 → 64%.
- **Bonferroni** (α/m) controls FWER, is conservative. **Holm** is step-down, controls FWER, and is uniformly more powerful — there is no reason to prefer plain Bonferroni.
- **Benjamini–Hochberg** controls **FDR**, not FWER — the right choice when you're screening many metrics and can tolerate some false discoveries.
- The practical fix in industry is not a correction at all: **pre-register one primary metric**, treat the rest as guardrails or exploratory, and require a replication run for anything found in the tail.
- The multiplicity is often hidden: 12 metrics × 5 segments × 3 time windows = 180 tests, none of which were declared.

**THE FOLLOW-UP:** *"We ran 10 variants; one won with p < 0.05. Would you ship it?"* and *"We track 12 metrics and declare a win if any hits p < 0.05 — what's wrong and how would you redesign it?"* (Both are real: the first from Emma Ding's bank, the second is Uber's.) Good answer: quantify the inflated FWER, name Holm or BH, then say the *design* fix — one primary metric declared in advance, plus a confirmation run for the winner.

**THE TRAP:** Applying Bonferroni to 12 *correlated* metrics and calling it done — you are now badly underpowered and you still haven't addressed the segment slicing. Also: correcting the metrics but not the segments.

**REAL FAILURE:** Bennett et al.'s dead-Atlantic-salmon fMRI study (2009, Ig Nobel 2012). Scanning a **dead fish** and testing ~130,000 voxels uncorrected produced a cluster of "active" voxels in the salmon's brain cavity at p < 0.001. It was built as an argument for mandatory multiple-comparison correction in neuroimaging. ([poster PDF](https://prefrontal.org/files/posters/Bennett-Salmon-2009.pdf))

---

## C7. Which Test, and When the Standard Choice Is Wrong
**Kicker:** Naming the test is table stakes; naming the assumption that's about to break is the answer.

- **Welch's t-test is the correct default** for two means, not Student's — it doesn't assume equal variances and costs almost nothing when they are equal.
- **Two-proportion z-test** only when each user contributes one observation. If users contribute many events, you need clustered SEs or the delta method.
- **Chi-square** for contingency tables and for **SRM checks**; switch to **Fisher's exact** when expected cell counts drop below ~5.
- **Mann–Whitney** for skewed data — but it tests stochastic dominance, so don't use it and then report a mean lift.
- **KS test** is fine for two moderate samples and useless as a production drift alarm at scale (see P8).
- **Paired** tests wherever the design is paired: same users before/after, same eval questions across two models, same query across two rankers. Pairing removes a huge variance component.

**THE FOLLOW-UP:** *"Your metric is revenue per user, it's zero-inflated and heavy-tailed, and you have 30k users per arm. Walk me through the test you'd actually run."* (Options in order: cap/winsorize and Welch; or bootstrap the difference in means at the user level; or decompose into P(purchase) × E[revenue | purchase] and test both; or CUPED to cut variance first. Say which and why.)

**THE TRAP:** Reciting "if normal use t-test, else Mann-Whitney" as a flowchart. Also: running a Shapiro-Wilk normality test on 100k rows to decide — with that n it always rejects, and it's the *sampling distribution of the mean* that needs to be normal, not the data.

**REAL SYSTEM:** The delta method / cluster-robust equivalence is now standard in experimentation platforms precisely because the naive proportion test is wrong whenever randomisation unit ≠ analysis unit. ([Eppo docs](https://docs.geteppo.com/guides/advanced-experimentation/analyzing-clustered-experiments/))

---

## C8. The Bootstrap
**Kicker:** When there's no formula for the standard error of your statistic, resampling *is* the formula — as long as you resample the right thing.

- Resample n rows with replacement B times (B ≥ 1,000; 10,000 for tails), recompute the statistic, take percentiles for the CI.
- Works for medians, quantiles, ratios, AUC, win rates, F1, and every LLM eval metric — anything where the delta method is painful.
- **Resample clusters, not rows**, whenever data are grouped (users, sessions, documents). Otherwise you reproduce the independence lie from F3.
- Percentile bootstrap is fine most of the time; **BCa** corrects bias and skew; **smooth bootstrap** (bootstrap + KDE) is recommended for small-n eval scores.
- The bootstrap is **not** valid for the maximum of a selected set — bootstrapping "the best of 12 prompts" without a max-T correction gives you an interval around a number that was chosen for being lucky.

**THE FOLLOW-UP:** *"Your eval metric is a median latency, n = 200. Give me a 95% CI."* → bootstrap. Then: *"Now the 200 traces come from 20 users. Does anything change?"* → resample users, not traces.

**THE TRAP:** Bootstrapping rows in clustered data; using too few resamples for a tail quantile; and bootstrapping a selected maximum.

**REAL SYSTEM:** `statsforevals.com` recommends the **smooth bootstrap** as "the most reliable general-purpose method" for non-binary eval scores, and explicitly flags that bootstrap CIs on selection-biased results (e.g. best prompt from a sweep) need a **max-T correction**. ([statsforevals.com/resources](https://statsforevals.com/resources.html))

---

## C9. Zero Events, Tiny Rates, and the Rule of Three
**Kicker:** "We saw zero failures in 300 runs" is not the same as "the failure rate is zero," and the rule of three tells you exactly how not-the-same.

- With 0 events in n trials, the 95% upper confidence bound on the rate is approximately **3/n**.
- 0 jailbreaks in 300 red-team prompts ⇒ the true rate could still be **1%**. 0 in 1,000 ⇒ up to 0.3%. To bound a rate below 0.1% you need ~3,000 clean trials.
- Derivation to state: (1−p)^n = 0.05 ⇒ n·ln(1−p) = ln(0.05) ⇒ p ≈ 3/n for small p. It's the ln(20) ≈ 3 trick.
- For non-zero small counts, use **Wilson** or Clopper-Pearson intervals, never Wald (which can produce negative lower bounds).
- Rare-event A/B tests are brutally underpowered: at p = 0.001, detecting a 10% relative change needs roughly 16·0.001·0.999/0.0001² ≈ **1.6 million per arm**.

**THE FOLLOW-UP:** *"Safety review says the model produced zero policy violations in 500 evaluation prompts. Can we ship?"* (Upper bound ≈ 0.6%. At 10M requests/day that's up to 60,000 violations/day. Reframe: what rate is acceptable, and how many clean trials does that require?)

**THE TRAP:** Reporting 0/500 as "0% failure rate" with no interval; or computing a Wald interval that gives [0, 0].

**REAL FAILURE / SOURCE:** The rule of three's canonical treatment is Jovanovic & Levy, *The American Statistician* 51(2), 1997, and Hanley & Lippman-Hand's 1983 *JAMA* paper "If nothing goes wrong, is everything all right?" — written because clinical trials were reporting zero adverse events as evidence of safety. ([Jovanovic & Levy PDF](http://www.nicksun.fun/assets/misc_papers/Jovanovic_1997_A_look_at_the_rule_of_three_The_American_Statistician.pdf))

---

## C10. The Winner's Curse (Type M and Type S Errors)
**Kicker:** The lift you ship is systematically bigger than the lift you get, and the reason is that you selected it for being big.

- Observed effect = true effect + noise. Selecting the maximum selects partly on the noise, so the estimate is biased **upward** — regression to the mean with a business consequence.
- **Type M (magnitude) error**: the exaggeration ratio of the estimate vs the truth under selection on significance. **Type S (sign) error**: probability a "significant" effect has the wrong sign. Both from Gelman & Carlin (2014).
- Empirically: shipped-win effects shrink **20–50%** in production. Facebook News Feed (Coey & Cunningham 2019, 226 tests): shrinkage estimators cut MSE by **44%**. Airbnb (Lee & Shen 2018) documented **20–50%** portfolio-level overstatement.
- Fixes: **empirical-Bayes shrinkage** of the reported lift, a **replication/holdback** run, or discounting the roadmap forecast by a known shrinkage factor.
- This is why "we shipped 30 experiments worth +1% each, so we should be up 30%" never comes true.

**THE FOLLOW-UP:** *"Your test showed a 1% improvement. Should you expect the same 1% after launch?"* (No. Name regression to the mean, quote the 20–50% shrinkage range, propose a shrunk estimate or a post-launch holdback to measure the realised effect.)

**THE TRAP:** Attributing the shrinkage entirely to "novelty effect." Novelty is a *different* mechanism (P5) and both can be present — you should name both and say how you'd distinguish them (novelty shows a time trend within the test; winner's curse does not).

**REAL FAILURE:** The gap between summed experiment lifts and observed annual metric movement is a documented, universal problem in experimentation orgs — Kohavi/Tang/Xu treat it as a standard hazard, and Azevedo et al. (2020) modelled the true-effect distribution across Bing's portfolio to correct it. ([atticusli.com winner's curse, with citations](https://atticusli.com/replication-crisis/ab-testing-winners-curse/))

---

## C11. Simpson's Paradox and the Segment That Flips
**Kicker:** Every subgroup can move one way while the aggregate moves the other, and the aggregate is not automatically the truth.

- Mechanism: an unequal mix across a confounding variable. The aggregate is a weighted average, and the weights differ between groups.
- Canonical case: UC Berkeley 1973 graduate admissions — **44% of men admitted vs 35% of women** in aggregate, but department-by-department women were admitted at *equal or higher* rates. Women applied disproportionately to departments with low admission rates overall. ([Bickel, Hammel & O'Connell, *Science* 187:398, 1975](https://www.science.org/doi/10.1126/science.187.4175.398))
- In experiments the same shape appears as **mix shift**: if your treatment changes the composition of who is active, segment-level and overall results diverge.
- Which number is right depends on the causal question, not the arithmetic. Drawing the DAG resolves it; the data alone cannot.
- The practical version: always pre-register a segment plan, and treat post-hoc segment findings as hypothesis-generating.

**THE FOLLOW-UP:** *"The overall lift is significantly positive, but for your largest customer segment it's significantly negative. What do you do?"* (Spotify's question. Check for SRM within segments; check whether the segment split is defined by a post-treatment variable; decide whether the segment loss is a launch blocker; propose a targeted rollout and a confirmation test — do not just average it away.)

**THE TRAP:** Slicing into 15 segments *after* seeing a null result and reporting the one that's significant, which is C6 in disguise. Also: segmenting on a variable measured **after** treatment (a collider), which manufactures paradoxes.

**REAL FAILURE:** The Berkeley case is the textbook example precisely because the university was facing a discrimination suit on the aggregate number; the statistical reanalysis found the disparity was mostly explained by department choice — an answer that is neither "there's no bias" nor "the aggregate was right." ([refsmmat.com's careful reading](https://www.refsmmat.com/posts/2016-05-08-simpsons-paradox-berkeley.html))

---

## C12. Practical vs Statistical Significance
**Kicker:** With 10 million users everything is significant; the interesting question is whether it matters.

- p-values shrink with n; effect sizes don't. At Facebook scale, a Cohen's d of 0.001 clears p < 0.001.
- Always report the effect with its CI and compare it to a pre-declared decision threshold, not to zero.
- Effect size vocabulary worth having: Cohen's d, relative lift, absolute lift, ROI per user, and "does this clear the cost of maintaining the feature."
- The inverse error is equally common: dismissing a 0.3% lift as "small" when 0.3% of revenue is $40M/year.
- The honest framing is a decision problem: expected value of shipping vs cost of complexity vs risk on guardrails.

**THE FOLLOW-UP:** *"p < 0.001 and the lift is 0.02%. Ship?"* (Depends entirely on cost and guardrails. State the decision rule you'd have written down before the test.)

**THE TRAP:** Using "statistically significant" as a synonym for "important," or arguing from p-value size ("p = 0.0001 is a stronger effect than p = 0.04" — no, it's a more precisely estimated one, possibly of a smaller effect).

**REAL FAILURE:** Facebook's emotional contagion experiment (Kramer, Guillory & Hancock, *PNAS* 111(24), June 2014) manipulated News Feed for **689,003 users**. The effects were real and highly significant — and Cohen's d was around 0.001, i.e. roughly one fewer emotional word per thousand. The paper became famous for its ethics; the statistical lesson is that "massive-scale" and "significant" say nothing about magnitude. ([PNAS](https://www.pnas.org/doi/10.1073/pnas.1320040111))

---

## C13. The Base Rate of True Hypotheses (Why Most Findings Are False)
**Kicker:** If most of your ideas are wrong, then most of your "significant" results are also wrong — and you can compute exactly how wrong.

- With α = 0.05 and power = 0.80, the positive predictive value of a significant result is `0.8π / (0.8π + 0.05(1−π))`, where π is the prior probability an idea is real.
- π = 1/3 → PPV = **89%**. π = 1/500 → PPV = **3.1%**. Kohavi runs this exact calculation for Bing.
- Ioannidis (2005) generalised it with bias and multiple-team terms — the origin of "Why Most Published Research Findings Are False," now one of the most-cited PLoS Medicine papers ever.
- Practical consequences: raise π (better hypotheses, prior evidence), raise power, lower α for surprising claims, and **replicate** anything that surprises you.
- This is the statistical justification for **Twyman's law**: "any figure that looks interesting or different is usually wrong."

**THE FOLLOW-UP:** *"Your test shows a +12% lift on a core metric. What's your first reaction?"* (Correct answer: disbelief. Check SRM, check instrumentation, check for a bug that inflates the treatment's event logging, then check whether the effect is concentrated in one day/browser/country. Only then celebrate.)

**THE TRAP:** Treating a big, surprising win as the good outcome. In a mature experimentation org a +12% lift is a bug report until proven otherwise.

**REAL FAILURE:** Amgen (Begley & Ellis, *Nature* 483:531, March 2012) attempted to reproduce **53 "landmark" preclinical cancer studies** and confirmed the findings in only **6** — about 11%. Bayer reported a similar 20–25% figure in 2011. Both are the PPV formula playing out at scale. ([*Nature* 483:531](https://www.nature.com/articles/483531a))

---
# TIER 3 — ADVANCED (Bayesian, causal, regression diagnostics)

---

## A1. Bayesian Inference: The Prior Is the Whole Argument
**Kicker:** Bayesian methods give you the probability statement everyone wants — at the price of having to defend a prior in public.

- Posterior ∝ likelihood × prior. A **credible interval** *is* the statement "95% probability the parameter is in here, given the model and prior" — the thing people wrongly say about CIs.
- Conjugate pairs worth knowing: Beta–Binomial (conversion rates), Gamma–Poisson (counts), Normal–Normal (means). Beta(1,1) is uniform; Beta(α,β) is "α−1 prior successes, β−1 prior failures."
- Bayesian shrinkage is the principled fix for the winner's curse and for sparse-segment estimates (hierarchical/partial pooling).
- With a lot of data, priors wash out and Bayesian and frequentist intervals converge — the argument matters most exactly where data are thin, i.e. small eval sets and new-market launches.
- The honest limitation: an informative prior is a *choice*, and a stakeholder can reasonably reject it. Be able to show a sensitivity analysis across priors.

**THE FOLLOW-UP:** *"You're launching in a new city with almost no data. Construct a prior."* (Uber's question. Answer: hierarchical model pooling across existing cities, with the new city's prior centred on the population mean and a variance set by the between-city variance. Then show how much the posterior moves under a flat prior vs your informative one.)

**THE TRAP:** Presenting a Bayesian result as assumption-free ("it just gives the probability"), or picking Beta(1,1) and calling it "no prior" — a uniform prior on a rate is an informative statement about the odds scale.

**REAL SYSTEM:** `statsforevals.com` recommends **Bayesian paired methods for pairwise binary comparisons at small N (<100)**, switching to bootstrap above that — a concrete, defensible boundary for when Bayes earns its keep in LLM eval work. ([statsforevals.com](https://statsforevals.com/resources.html))

---

## A2. Bayesian A/B Testing and Expected Loss
**Kicker:** "95% probability B beats A" sounds like the answer to everything, and it silently hides how much you lose if you're wrong.

- Bayesian A/B gives P(B > A) and the posterior distribution of the lift — valid at any sample size, no peeking correction needed for the *posterior* itself.
- But P(B>A) = 0.96 with a lift of +0.01% is a terrible reason to ship. The decision quantity is **expected loss**: `E[max(0, θ_A − θ_B)]` — how much you expect to give up by choosing B.
- Standard rule: ship when expected loss falls below a pre-set threshold of caring (e.g. 0.1% of the metric).
- Bayesian methods do not exempt you from **stopping-rule discipline**: if you stop as soon as P(B>A) > 0.95 with a flat prior, your long-run error behaviour is close to frequentist peeking. The posterior is coherent; your *decision procedure* still has operating characteristics you should simulate.
- VWO and GrowthBook ship Bayesian engines; Optimizely, Statsig, Eppo and Spotify are frequentist-sequential. Know that the industry is genuinely split.

**THE FOLLOW-UP:** *"Your Bayesian engine says 96% chance B wins. The frequentist p-value is 0.09. Which do you believe, and what do you tell the PM?"* (They're answering different questions and both are 'right'; the decision hinges on the prior, the loss function and whether the CI/credible interval excludes your MDE. Show the interval, not the probability.)

**THE TRAP:** Claiming Bayesian A/B "solves peeking." It removes the *multiple-testing interpretation problem*, not the fact that an early-stopping rule changes the distribution of decisions you make.

**REAL SYSTEM:** Expected-loss decision rules are the documented default in Bayesian experimentation platforms. ([GrowthBook Bayesian docs](https://www.growthbook.io/insights/bayesian-statistics); [expected loss explainer](https://donnuab.com/blog/en/expected-loss-in-bayesian-ab-testing/))

---

## A3. Confounding, DAGs and the Backdoor Criterion
**Kicker:** "I threw everything into the regression" is the most common way to make a causal estimate worse.

- Draw the DAG. Confounder (common cause of X and Y) → **must** control. Mediator (on the path X→M→Y) → controlling removes the effect you wanted. Collider (common effect) → controlling **creates** spurious association.
- **Bad controls** are a named failure: conditioning on a post-treatment variable biases the estimate, sometimes reversing its sign.
- **Berkson's paradox / collider bias**: in a sample selected on "admitted" or "hospitalised" or "clicked," two independent causes become negatively correlated.
- The backdoor criterion tells you the minimal sufficient adjustment set; it is a graph question, not a p-value question.
- Say "pre-treatment covariates only" and you've dodged 80% of the trap.

**THE FOLLOW-UP:** *"You're estimating the effect of Instant Book on host bookings and you control for number of enquiries. Is that OK?"* (Airbnb's question. No — enquiries are downstream of Instant Book; it's a mediator/bad control. You'd be estimating a direct effect conditional on a post-treatment variable and inducing collider bias.)

**THE TRAP:** "More controls = less bias." Also: controlling for a variable *because it improved R²*, which is a predictive criterion applied to a causal question.

**REAL FAILURE:** Obermeyer et al., *Science* 366:447 (Oct 2019). A commercial risk-prediction algorithm used on roughly **200 million people per year** in the US predicted **healthcare cost** as a proxy for health need. Because less money was historically spent on Black patients at the same level of illness, Black patients had to be considerably sicker to get the same risk score. Correcting the label raised the fraction of Black patients receiving extra care from **17.7% to 46.5%**. The bug was the *choice of outcome variable*, not the model. ([*Science* 366:447](https://www.science.org/doi/10.1126/science.aax2342))

---

## A4. Regression Diagnostics That Actually Matter
**Kicker:** Nobody will ask you to recite the Gauss–Markov assumptions; they will hand you a residual plot and ask what's broken.

- The five OLS assumptions: linearity, low multicollinearity, normally distributed errors, homoscedasticity, independent errors. The last two are the ones that break in practice.
- **Heteroscedasticity** doesn't bias coefficients, it biases *standard errors* — so use **robust (HC3) SEs** by default. Same for **clustered** errors when data are grouped.
- **Multicollinearity** doesn't bias coefficients either — it inflates their variance, which makes individual coefficients unstable and uninterpretable while predictions stay fine. VIF > 5–10 is the usual flag.
- Normality of *errors* matters only for small-sample inference; with n large the CLT covers the coefficient estimates.
- The diagnostic that actually catches bugs: plot residuals vs fitted, residuals vs each feature, and residuals vs time.

**THE FOLLOW-UP:** *"Your ad-conversion model has two features correlated at 0.95. One coefficient is significantly positive, the other significantly negative. What's going on and does it matter?"* (Meta's question. Multicollinearity: the coefficients are individually unidentified but jointly fine. If you only need prediction, ignore it; if you need to interpret, drop one, combine them, or regularise — and say which.)

**THE TRAP:** "The residuals aren't normal so my regression is invalid." Usually irrelevant. Meanwhile the actual problem — non-independent errors from repeated measures — goes unmentioned.

**REAL FAILURE:** Reinhart & Rogoff's *Growth in a Time of Debt* (2010) claimed growth turns sharply negative above a 90% debt-to-GDP ratio. Herndon, Ash & Pollin (UMass Amherst, April 2013) found a spreadsheet range error excluding five countries, selective data exclusion, and an unconventional weighting scheme. Corrected, average growth above 90% debt was **+2.2%, not −0.1%**. The paper had been cited in austerity policy across Europe and the US. ([PERI/UMass critique](https://peri.umass.edu/publication/does-high-public-debt-consistently-stifle-economic-growth-a-critique-of-reinhart-and-rogoff/); [Retraction Watch](https://retractionwatch.com/2013/04/18/influential-reinhart-rogoff-economics-paper-suffers-database-error/))

---

## A5. ROC-AUC vs PR-AUC vs Calibration
**Kicker:** ROC-AUC is the metric that looks good on imbalanced data precisely because it ignores the thing that makes imbalanced data hard.

- ROC plots TPR vs FPR. FPR has the (huge) negative class in its denominator, so a flood of false positives barely moves it. PR curves put precision — which has the *predicted positives* in the denominator — on the y-axis, so they react.
- With 0.1% positives, a model with AUC 0.95 can still have precision under 5% at any useful recall. Saito & Rehmsmeier (PLoS ONE, 2015) is the standard citation.
- **AUC is rank-based and says nothing about calibration.** A model can have perfect AUC and be wildly miscalibrated (all probabilities squashed into [0.4, 0.6]).
- Calibration metrics: reliability diagram, **Brier score** (proper scoring rule, decomposes into calibration + refinement), **ECE** (binned, sensitive to binning). Fix with Platt scaling or isotonic regression on a held-out set.
- If a downstream decision uses the probability (expected value, thresholding on cost), calibration matters more than AUC.

**THE FOLLOW-UP:** *"Your fraud model has AUC 0.97 but the ops team says the queue is full of garbage. Diagnose it."* (Prevalence: compute precision@k at the operating threshold, plot the PR curve, check calibration at the top of the ranking, and reconsider whether AUC was ever the right metric.)

**THE TRAP:** Reporting AUC on a class-rebalanced test set. Rebalancing the *training* set is a modelling choice; rebalancing the *test* set makes every downstream precision estimate a fiction.

**REAL FAILURE:** The Epic Sepsis Model. Wong et al. (*JAMA Internal Medicine*, June 2021) externally validated it on **38,455 hospitalisations / 27,697 patients** at Michigan Medicine (Dec 2018–Oct 2019). Epic advertised AUC **0.76–0.83**; the measured AUC was **0.63** (95% CI 0.62–0.64). At the recommended threshold: sensitivity **33%**, PPV **12%**; it **missed 67% of sepsis cases** (1,709 of 2,552) while alerting on 18% of all hospitalisations. The model was deployed at hundreds of US hospitals. ([PMC8218233](https://pmc.ncbi.nlm.nih.gov/articles/PMC8218233))

---

## A6. Fairness Metrics Are Mutually Incompatible
**Kicker:** You cannot have equal false-positive rates, equal false-negative rates and calibration at the same time unless base rates are equal — this is a theorem, not a tradeoff you can engineer around.

- Kleinberg, Mullainathan & Raghavan (2016) and Chouldechova (2017) independently proved the impossibility: calibration within groups, equal FPR and equal FNR cannot all hold when prevalence differs across groups.
- So "is it fair?" is unanswerable until someone picks *which* fairness definition the product owes its users.
- The practical implication for an ML engineer: the choice of fairness metric is a policy decision that must be made explicitly and written down, not discovered in a fairness library's defaults.
- Related: **intersectional** error analysis. Aggregate accuracy hides subgroup catastrophe.
- The statistical skill being tested is disaggregated evaluation with confidence intervals per subgroup — small subgroups have wide intervals and you must say so.

**THE FOLLOW-UP:** *"Your model is calibrated within both groups but has a higher false-positive rate for one. Is it biased?"* (Both statements can be simultaneously true and it's a theorem, not a bug. Ask which harm the product is optimising against.)

**THE TRAP:** Claiming a model is "fair" because a single metric passed, or claiming ProPublica or Northpointe was simply "wrong" — they measured different, mutually exclusive things.

**REAL FAILURE:** ProPublica's COMPAS analysis (May 2016) found Black defendants were roughly twice as likely to be falsely flagged high-risk (~45% vs ~23% FPR), while Northpointe showed the score was calibrated — equal recidivism rates at equal scores — across race. Both were arithmetically correct. Chouldechova's paper formalised why. ([ProPublica methodology](https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm)); intersectional version: Buolamwini & Gebru's *Gender Shades* (FAT* 2018) found commercial gender classifiers erred on **darker-skinned women up to 34.7%** of the time vs **0.8%** for lighter-skinned men. ([PMLR v81](https://proceedings.mlr.press/v81/buolamwini18a.html))

---

## A7. Quasi-Experiments: Diff-in-Diff, Synthetic Control, RDD
**Kicker:** Half of production questions cannot be randomised, and "we couldn't A/B test it" is not an acceptable stopping point in 2026.

- **Difference-in-differences**: compare the change over time in treated vs untreated units. Identifying assumption is **parallel trends** — testable only in the pre-period, and that test is weak.
- **Synthetic control**: build a weighted combination of untreated units that matches the treated unit's pre-period, then compare post. Good for one-market rollouts.
- **Regression discontinuity**: exploit a threshold (score ≥ 700 gets the offer) to estimate a local effect right at the cutoff. Only local, and only if units can't manipulate the running variable.
- **Interrupted time series** with proper seasonality handling; **instrumental variables** for non-compliance.
- All of them buy identification with assumptions. Say the assumption out loud and say how you'd stress-test it (placebo periods, placebo units, pre-trend tests).

**THE FOLLOW-UP:** *"You launched in Germany only and want the causal impact. There's no control group. What do you do, and what would make your answer wrong?"* (Synthetic control from other EU markets; wrong if Germany had a market-specific shock, if the donor pool markets were themselves affected by the launch, or if pre-period fit is poor.)

**THE TRAP:** Running diff-in-diff without ever plotting the pre-trends, or including in the donor pool a market that was also treated (spillover).

**REAL SYSTEM:** Netflix published its quasi-experimentation program specifically for cases where randomisation is impossible — content launches, marketing spend, region-level changes — along with a companion post on the key challenges (parallel trends, few units, interference). ([Netflix TechBlog: Quasi Experimentation at Netflix](https://netflixtechblog.com/quasi-experimentation-at-netflix-566b57d2e362); [Key Challenges](https://netflixtechblog.com/key-challenges-with-quasi-experiments-at-netflix-89b4f234b852))

---

## A8. Data Leakage Is a Statistical Failure, Not a Coding Bug
**Kicker:** Leakage is the ML-specific way of computing a confidence interval around a number that could never occur in production.

- Eight named types (Kapoor & Narayanan): no test set at all; pre-processing (scaling/imputation) fitted on the full data; feature selection on the full data; duplicates across splits; illegitimate features (proxies for the label); temporal leakage; non-independence between train and test; sampling bias in the test set.
- Time-series and grouped data need **temporal** and **group-aware** splits. Random k-fold on user-level data leaks the user.
- The tell: a model that's suspiciously good. Twyman's law applies to offline metrics too.
- Leakage inflates the *point estimate*; it also destroys the meaning of every CI you compute afterwards.
- Fix: build the split first, wrap all preprocessing in a pipeline fitted inside the fold, and hold out a truly untouched final set.

**THE FOLLOW-UP:** *"Your churn model gets 0.94 AUC offline and 0.61 in production. Give me your top three hypotheses, ranked."* (1: temporal/target leakage — a feature populated only after churn; 2: train/serve skew in feature computation; 3: distribution shift / different population. Then say how you'd test each.)

**THE TRAP:** "I used cross-validation so there's no leakage." CV with preprocessing fitted outside the loop leaks in every fold.

**REAL FAILURE:** Kapoor & Narayanan, *Patterns* 4(9), Sept 2023: leakage-driven errors found across **17 scientific fields, collectively affecting 329 papers**. In their civil-war-prediction case study, *every* paper claiming complex ML beat logistic regression failed to reproduce once leakage was fixed — the decades-old LR baseline was as good. ([arXiv:2207.07048](https://arxiv.org/abs/2207.07048); [Patterns](https://www.cell.com/patterns/fulltext/S2666-3899(23)00159-9))

---

## A9. Distribution Shift and the Confound You Learned Instead
**Kicker:** A model's test accuracy is a statement about a distribution, and the distribution in production is not the one you measured.

- Three named shifts: **covariate shift** (P(X) changes), **label shift** (P(Y) changes), **concept drift** (P(Y|X) changes). Only the third needs a new model; the first two often need reweighting or recalibration.
- Models learn whatever is predictive, including site, scanner, timestamp watermark, template, or which team wrote the label.
- The evaluation fix: **external validation** on a genuinely different source, and **stratified metrics** by every plausible source of shift.
- The 1/√n intuition applies to subgroup metrics too — subgroup CIs are wide, so "no difference across sites" often just means "underpowered per site."
- In LLM systems the equivalent is: your eval set is 200 curated prompts and production is a long tail of typos, other languages, and adversarial input.

**THE FOLLOW-UP:** *"Your medical imaging model gets 0.93 AUC internally. What single experiment would you run before believing it?"* (Train on site A, test on site B. Then train a classifier to predict *site* from the image — if it's near-perfect, your model has a shortcut available.)

**THE TRAP:** Reporting a random-split test score for a model that will be deployed at a new hospital, store, region or customer, and calling that "held out."

**REAL FAILURE:** Zech et al., *PLOS Medicine* (6 Nov 2018). A pneumonia CNN scored AUC **0.802** internally at Mount Sinai but only **0.717** at NIH. Pneumonia prevalence was **34.2%** at MSH vs **1.2%** at NIH, and a CNN could identify the source hospital from the radiograph with **99.95%** accuracy — a trivial hospital-prevalence-only model reached AUC **0.861** on the combined data. ([PLOS Medicine](https://journals.plos.org/plosmedicine/article?id=10.1371%2Fjournal.pmed.1002683)) Companion: Roberts et al., *Nature Machine Intelligence* (March 2021) reviewed **2,212 COVID-19 imaging ML papers**, kept 62 after screening, and found **none** were of potential clinical use — largely due to "Frankenstein" datasets, duplicated images across splits, and no external validation. ([Nature MI](https://www.nature.com/articles/s42256-021-00307-0))

---

## A10. Metric Choice Manufactures Findings
**Kicker:** Change the metric and the phenomenon appears or vanishes — which means the metric is part of your claim, not a neutral instrument.

- Discontinuous metrics (exact-match, all-or-nothing accuracy) turn smooth improvements into apparent step changes. Continuous metrics (token edit distance, log-likelihood) show the same underlying progress as smooth.
- Same mechanism in classic ML: thresholded metrics (accuracy, F1 at 0.5) hide changes that AUC or log-loss reveal, and vice versa.
- Aggregation choices matter as much: macro vs micro averaging, per-user vs per-event, capped vs uncapped.
- Always ask "what does this metric do to a model that is 90% right on every item vs 100% right on 90% of items?"
- **Goodhart's law** is the production form: once a metric is a target, optimisation pressure moves the metric without moving the thing.

**THE FOLLOW-UP:** *"Your win rate against the baseline went from 48% to 61% but average judge score barely moved. Which do you report?"* (Both, plus the distribution. A win-rate jump with a flat mean usually means many small wins near the decision boundary — check whether the judge has a tie-breaking bias or a verbosity preference.)

**THE TRAP:** Treating benchmark scores as properties of the model rather than of the (model, metric, prompt, parser) tuple.

**REAL FAILURE:** Schaeffer, Miranda & Koyejo, *Are Emergent Abilities of Large Language Models a Mirage?* (NeurIPS 2023). They showed that "emergent" capability jumps largely disappear when nonlinear/discontinuous metrics are replaced with linear/continuous ones on the same model outputs — and that they can be *induced* in domains where nobody claims emergence, purely by choosing a discontinuous metric. ([arXiv:2304.15004](https://arxiv.org/abs/2304.15004); [NeurIPS PDF](https://papers.neurips.cc/paper_files/paper/2023/file/adc98a266f45005c403b8311ca7e8bd7-Paper-Conference.pdf))

---

## A11. Uncertainty in the Model, Not Just the Data
**Kicker:** Two models with the same accuracy can disagree wildly about which examples they're unsure of, and only one of them is safe to route on.

- Decompose: **aleatoric** uncertainty (irreducible noise in the data) vs **epistemic** uncertainty (reducible by more data). Only epistemic uncertainty is fixed by collecting more.
- Cheap estimators: deep ensembles (strongest baseline), MC dropout, bootstrap over training sets, conformal prediction for distribution-free coverage guarantees.
- **Conformal prediction** is the one worth naming in 2026: given exchangeability, it gives a prediction *set* with guaranteed marginal coverage at level 1−α with no distributional assumptions. Useful for abstention and human routing.
- For LLMs: token-level log-probs are a usable but poorly calibrated confidence signal; self-reported confidence is worse; ensembling over samples (self-consistency) is better.
- Random seed variance is a real, measurable component — Bouthillier et al. (2021) showed seed-to-seed variation threatens benchmark conclusions.

**THE FOLLOW-UP:** *"You want the model to abstain on the hardest 5% of inputs. How do you pick them, and how do you know your abstention policy is working?"* (Conformal or ensemble disagreement to rank; then evaluate on the *retained* set's accuracy vs coverage curve, with CIs — and check the abstained set isn't just one demographic or one language.)

**THE TRAP:** Using the softmax max-probability as "confidence" on a network that was never calibrated, and building a routing threshold on it.

**REAL SYSTEM:** `statsforevals.com` cites Bouthillier et al. (2021) on seed variance as one of four foundational papers, alongside Demšar (2006) on non-parametric multi-dataset comparison and Miller (2024) on eval error bars. ([statsforevals.com](https://statsforevals.com/resources.html))

---
# TIER 4 — IN PRODUCTION (experimentation, monitoring, eval statistics)

---

## P1. Sample Ratio Mismatch: The First Thing You Check
**Kicker:** If the split isn't 50/50, nothing downstream is valid — and roughly 6% of real experiments fail this check.

- SRM = the observed allocation differs from the configured allocation by more than chance. Test with a **chi-square goodness-of-fit** on the user counts.
- Use a **very strict** threshold (p < 0.0005 or 0.001, not 0.05) because you run this check on every experiment and you want almost no false alarms — and because a real SRM is usually gross, not marginal.
- **~6% of experiments at Microsoft** had an SRM; at 10,000 experiments/year that's about one per day.
- The five-part taxonomy (Fabijan et al., KDD 2019) is worth memorising: **assignment** (randomisation bug, unstable IDs, correlated multi-experiment assignment), **execution** (delivery delay, telemetry loss, performance degradation), **log processing** (bot filtering, bad joins), **analysis** (wrong trigger/filter, incomplete counterfactual logging), **interference** (force-assignment via URL params, telemetry injection).
- Critically: an SRM means the *effect estimate* is untrustworthy in an unknown direction. You cannot "adjust for it."

**THE FOLLOW-UP:** *"You see 50.4% / 49.6% on 1.2 million users. Is that a problem?"* (Yes — chi-square p is astronomically small at that n. Then: *"Where would you look first?"* → is the imbalance present at assignment or only after filtering? If assignment is clean and analysis is skewed, the bug is in your trigger condition or bot filter, which means the treatment is changing who gets counted.)

**THE TRAP:** Two: (a) dismissing a small percentage imbalance because "it's only 0.4%"; (b) finding an SRM, excluding the affected users, and continuing — the exclusion is itself correlated with treatment.

**REAL FAILURE:** Named Microsoft cases from the KDD 2019 paper: **MSN Carousel** — the bot-detection algorithm flagged *engaged* treatment users as bots, masking a genuinely positive result. **Skype Audio** — a mid-session configuration refresh corrupted variant-ID logging and lost 30% of treatment sessions. **Microsoft Teams** — First-Run-Experience filtering excluded eligible users from triggered analysis. **Microsoft Store** — a search-campaign misconfiguration force-assigned users to one variant. ([Fabijan et al., KDD 2019](https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf))

---

## P2. CUPED and Variance Reduction
**Kicker:** The fastest way to shorten an experiment isn't more traffic — it's removing the variance you could have predicted before the experiment started.

- `Y_adj = Y − θ(X − E[X])` where X is a **pre-experiment** covariate and `θ = Cov(Y,X)/Var(X)`. The adjusted metric has the same expectation, so the estimate stays unbiased.
- Variance drops by a factor of `(1 − ρ²)`. ρ = 0.7 removes ~51% of variance ⇒ roughly **half the sample size** or half the runtime.
- The natural X is the **same metric in the pre-period**. For new users there is no pre-period, which is exactly why CUPED helps least where you often need it most.
- Extensions a 2026 candidate should be able to name: post-stratification, **control variates from an ML prediction of Y** (predicted-covariate CUPED), and 2024+ methods combining pre- and in-experiment data.
- Hard rule: the covariate must be measured **before** assignment. Using an in-experiment covariate reintroduces bias — this is the bad-control problem from A3.

**THE FOLLOW-UP:** *"CUPED cut your variance by 40% on returning users but did nothing for new users. What now?"* (Segment: apply CUPED to returners, use covariates available at assignment time for new users — device, geo, acquisition channel — via post-stratification or regression adjustment. Report the two segments separately or use a stratified estimator.)

**THE TRAP:** Describing CUPED as "controlling for pre-experiment differences to fix imbalance." It is a **variance reduction** technique, not a bias correction; randomisation already handles imbalance in expectation.

**REAL SYSTEM:** Deng, Xu, Kohavi & Walker, *Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data* (WSDM 2013) — the origin paper, from Bing. Now productised across Optimizely, Statsig and Eppo. ([WSDM 2013 PDF](https://exp-platform.com/Documents/2013-02-CUPED-ImprovingSensitivityOfControlledExperiments.pdf); [Optimizely docs](https://support.optimizely.com/hc/en-us/articles/33424529987597-CUPED-Controlled-experiment-Using-Pre-Experiment-Data))

---

## P3. Randomisation Unit ≠ Analysis Unit
**Kicker:** You randomised users but you're analysing clicks-per-impression, and your standard error is now a work of fiction.

- If you randomise by user and analyse per-event, events within a user are correlated. Naive SEs are too small, sometimes by 2–5×, and your A/A test will fire constantly.
- Two correct treatments: the **delta method** for ratio metrics, or **cluster-robust standard errors**. They are provably equivalent for clustered randomised experiments.
- Delta method for a ratio `R = X̄/Ȳ`: `Var(R) ≈ (1/μ_Y²)Var(X) − (2μ_X/μ_Y³)Cov(X,Y) + (μ_X²/μ_Y⁴)Var(Y)`, all computed at the user level.
- The alternative is to **aggregate first**: compute the ratio per user, then t-test the per-user ratios. This changes the estimand (average of ratios vs ratio of averages) — say which one the business wants.
- Same problem, other names: session-level metrics with user randomisation; tenant/account randomisation in B2B; per-query metrics with per-user assignment.

**THE FOLLOW-UP:** *"Would clicks-per-user and clicks-per-impression give you the same conclusion?"* (Not necessarily — a treatment that reduces impressions can raise CTR while lowering total clicks. Then: *"Which is the OEC?"*)

**THE TRAP:** Computing `sum(clicks)/sum(impressions)` and applying a two-proportion z-test with n = number of impressions. This is the single most common invalid test in production analytics.

**REAL SYSTEM:** Microsoft's experimentation group published specifically on why tenant-randomised A/B tests are hard and why tenant-pairing often fails — the B2B version of this problem, where you have hundreds of clusters rather than millions of users. ([Microsoft Research EXP](https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/why-tenant-randomized-a-b-test-is-challenging-and-tenant-pairing-may-not-work/); [delta method / CRVE equivalence](https://www.researchgate.net/publication/352016270_The_equivalence_of_the_Delta_method_and_the_cluster-robust_variance_estimator_for_the_analysis_of_clustered_randomized_experiments))

---

## P4. Interference: When SUTVA Breaks
**Kicker:** A/B testing assumes your treatment of me doesn't affect you — which is false in every marketplace and every social product.

- SUTVA (Stable Unit Treatment Value Assumption) requires no interference between units. Violated by: two-sided marketplaces (treatment consumes shared supply), social networks (treated users message untreated ones), shared budgets/inventory, and shared ML models retrained on treated traffic.
- Direction of the bias is not random: in a marketplace, treatment "steals" supply from control, so the measured lift **overstates** the global effect.
- Designs that fix it: **cluster randomisation** (randomise geos, markets, social clusters), **ego-cluster randomisation** (LinkedIn — randomise a user *and their neighbourhood*), **switchback / time-split** designs (Uber, DoorDash, Lyft — randomise time intervals across the whole market), and **budget-split** designs for ad auctions.
- The cost is always power: you go from millions of users to tens of clusters or hundreds of time slots, and your effective n collapses.

**THE FOLLOW-UP:** *"Independence between units is violated because of the social graph. Walk me through the design you'd use and what it costs you."* (Amplitude's/Emma Ding's question, in the wild. Name ego-clusters or graph clustering, then quantify: the effective sample size is the number of clusters, so your MDE grows by roughly √(users/clusters) × the design effect.)

**THE TRAP:** Saying "network effects" and stopping. The interviewer wants the *design*, the *direction of the bias*, and the *power cost*.

**REAL SYSTEM:** LinkedIn's ego-cluster randomisation (Saint-Jacques et al., arXiv:1903.08755, March 2019, with a 2023 follow-up improving cluster construction — [arXiv:2308.05945](https://arxiv.org/html/2308.05945v3)); DoorDash's switchback framework ([DoorDash Engineering](https://careersatdoordash.com/blog/switchback-tests-and-randomized-experimentation-under-network-effects-at-doordash/)); Lyft's marketplace marginal values approach to interference bias ([Lyft Engineering](https://eng.lyft.com/using-marketplace-marginal-values-to-address-interference-bias-a11aff6e670f)); Bojinov & Simchi-Levi on optimal switchback design ([HBS working paper](https://www.hbs.edu/ris/Publication%20Files/WP21-034_20160b13-a86c-4a0d-b6e9-bbae288486c5_c93009c0-8003-43fd-bb1a-012c02d33b98.pdf)).

---

## P5. Novelty, Primacy and Long-Term Effects
**Kicker:** The two-week experiment measures the two-week effect, and for anything users have to learn, that is not the effect you're shipping.

- **Novelty effect**: users engage with a change because it's new; the lift decays. **Primacy effect**: users are disrupted by a change; the deficit decays and the true effect is *larger* than measured. Both are time-varying treatment effects.
- Diagnose by plotting the treatment effect **by day since first exposure** (not calendar day) and by splitting new vs returning users. A decaying or growing curve is the signal.
- Google's ads-blindness work found a learning **half-life of about 60 days** — a 90-day study captures only ~65% of the total effect. A two-week test captures almost none of it.
- Long-run designs: **long-term holdbacks** (keep 1% in control for a quarter), **cookie-cookie-day randomisation** (re-randomise cookies daily so no cookie accumulates learning, giving you an unlearned baseline), staged rollouts, and post-launch holdouts.
- Google's headline result: a **50% reduction in mobile search ad load** showed significant short-term RPM losses but long-term effects settling near zero — the short-term test would have killed a change that was long-run neutral and user-positive.

**THE FOLLOW-UP:** *"Why did the effect decline after full launch?"* (Emma Ding's question. Answer with a ranked list: winner's curse / regression to the mean; novelty decay; the launch population differs from the experiment population; interference that disappears at 100%; seasonality; and instrumentation changes at launch. Then say how you'd tell them apart.)

**THE TRAP:** Attributing all shrinkage to novelty. Also: "we'll just run it for eight weeks" — that costs 4× the calendar and still doesn't reach the 60-day half-life; a holdback is cheaper.

**REAL SYSTEM:** Hohnhold, O'Brien & Tang, *Focusing on the Long-term: It's Good for Users and Business*, KDD 2015 — the source of the 60-day half-life, the cookie-cookie-day design, and the mobile ad-load result. ([Google Research PDF](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43887.pdf))

---

## P6. The OEC, Guardrails, and Trustworthiness
**Kicker:** The hardest part of an experiment is deciding, before you run it, what number would make you say no.

- **OEC** (Overall Evaluation Criterion): one primary metric, decided in advance, that the team agrees to be judged on. Everything else is secondary or guardrail.
- **Guardrail metrics** are things you must not break: latency, crash rate, unsubscribes, support tickets, revenue, and — for LLM products — refusal rate, hallucination rate, cost per request, p95 latency.
- Guardrails are tested for *non-inferiority*, not superiority. The question is "is the CI's lower bound above my tolerance?", not "is p < 0.05?".
- Kohavi's Rule 5 is the sobering one: multiple Bing experiments produced huge, significant click shifts with abandonment p-values of **0.64, 0.71, 0.83, 0.92, 0.93** — a 12% ad-revenue decline moved abandonment not at all. Some things are just very hard to move.
- **Twyman's law**: any figure that looks interesting or different is usually wrong. Institutionalise disbelief.

**THE FOLLOW-UP:** *"Your primary metric is up 0.8% (p = 0.01) and latency p95 is up 40 ms (p = 0.03). Ship?"* (This is a decision, not a test. State the pre-registered tolerance for latency; if 40 ms was inside tolerance you ship, if not you don't — and if nobody set a tolerance, that's the finding.)

**THE TRAP:** Inventing the OEC after seeing the results, or presenting a dashboard of 20 metrics and letting the PM pick. Also: treating a non-significant guardrail as "no harm" when the CI easily contains a serious regression (see C9 — absence of evidence).

**REAL SYSTEM:** Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* (Cambridge, 2020) is the reference text; the seven rules paper is the free, quotable version with all the numbers. ([Seven Rules of Thumb PDF](https://exp-platform.com/Documents/2014%20experimentersRulesOfThumb.pdf)); Booking.com's meta-experiments — experiments on their experimentation process itself — are the mature version. ([booking.ai](https://booking.ai/meta-experiments-improving-experimentation-through-experimentation-6bdee314c512))

---

## P7. Sensitivity: Interleaving and Proxy Metrics
**Kicker:** When your metric is too noisy to detect what you care about, the answer is usually a better *design*, not more traffic.

- **Interleaving** (team-draft): instead of showing user A ranker 1 and user B ranker 2, blend both rankers' results into one list for every user and attribute engagement back. Every user becomes their own control — a within-subject design.
- Netflix: interleaving needs **>100× fewer users** than a conventional metric A/B test to reach 95% power on ranking-quality comparisons.
- The limit: interleaving measures *relative preference between rankers*, not retention, revenue, or anything requiring a consistent product experience. Netflix uses it to *prune* candidates, then A/B tests the survivors.
- The general principle: **within-subject / paired designs remove the between-subject variance**, which is usually the dominant term. This is the same reason paired eval comparisons beat marginal CIs (C2).
- Other sensitivity levers, in rough order of payoff: pairing/interleaving → CUPED → capping/winsorising → better proxy metric → more traffic.

**THE FOLLOW-UP:** *"You need 6 weeks to detect your MDE and the team has 2. What are your options, ranked?"* (Interleaving or a paired design; CUPED; cap the metric; pick a more sensitive proxy correlated with the OEC; raise the MDE and say so explicitly; run a sequential design and accept the power cost. "Run it anyway and look at the trend" is the wrong answer.)

**THE TRAP:** Substituting a proxy metric without ever validating that it correlates with the OEC — proxy metrics need their own validation study.

**REAL SYSTEM:** Netflix's interleaving programme ([Netflix TechBlog, 2017](https://netflixtechblog.com/using-interleaving-in-online-experiments-to-accelerate-algorithm-innovation-at-netflix-a04ee392ec55)); replicated at Expedia and Thumbtack ([Thumbtack Engineering](https://medium.com/thumbtack-engineering/accelerating-ranking-experimentation-at-thumbtack-with-interleaving-20cbe7837edf)); Google's Pareto-optimal proxy metrics work for validating proxies against long-term outcomes ([arXiv:2307.01000](https://arxiv.org/html/2307.01000v2)).

---

## P8. Drift Monitoring: Why Your KS Test Alerts Every Day
**Kicker:** At production scale, a hypothesis test is a terrible alarm — with 10 million rows every trivial shift is p < 0.001.

- The p-value of any goodness-of-fit test goes to zero as n grows for *any* non-zero difference. KS, chi-square and Anderson-Darling all fail as monitoring alarms at scale.
- Use **effect-size thresholds** instead: **PSI** (Population Stability Index) with the conventional bands `< 0.1` = stable, `0.1–0.25` = moderate shift, `> 0.25` = significant shift; or Wasserstein distance, JS divergence, or a simple quantile-shift check.
- Alternatively, **subsample** to a fixed n (say 5,000) before testing so the alarm's sensitivity is constant over time.
- Distinguish what you're monitoring: **input drift** (P(X)) is cheap and early but often benign; **prediction drift** (P(Ŷ)) is a better proxy; **performance drift** (P(Y|X)) is what matters but needs labels, which arrive late or never.
- For LLM systems the equivalents are: prompt-distribution drift, judge-model drift (the judge itself got upgraded), and retrieval-corpus drift.

**THE FOLLOW-UP:** *"Your drift monitor fires on 8 of 40 features every day. What do you change?"* (Switch from p-values to PSI/effect size; correct for the 40 simultaneous tests with BH-FDR; tie the alarm to *prediction* or *performance* drift rather than input drift; and set the threshold from a backtest of historical days rather than a textbook default.)

**THE TRAP:** Alerting on statistical significance rather than magnitude, and then muting the whole system because it's noisy — which is how drift goes undetected for a quarter.

**REAL SYSTEM:** Evidently AI's comparison of five drift-detection methods on large datasets makes the point empirically: statistical tests become unusable at scale and distance metrics are the practical replacement. ([evidentlyai.com](https://www.evidentlyai.com/blog/data-drift-detection-large-datasets)); PSI band conventions ([StatsTest](https://www.statstest.com/drift-detection-ks-test-psi-interpret-signals)).

---

## P9. "We Ran It on 50 Prompts and Got 82%" Is Not a Result
**Kicker:** 82% on 50 prompts has a 95% confidence interval of roughly [71%, 93%] — you cannot distinguish it from 75% or from 90%.

- Bernoulli SE = `sqrt(p(1−p)/n)`. At p = 0.82, n = 50: SE = 5.4pp, so the 95% CI is about **[71%, 93%]** (wider still if you use Wilson, which you should at this n).
- To halve that interval you need **4× the data**. To resolve a 2-point difference between two models you need thousands of items — unless you pair (see P10/P12).
- Anthropic's five recommendations, which are now the de facto standard: (1) SEs from the CLT; (2) **clustered** SEs when questions come in related groups; (3) reduce variance by resampling answers and using next-token probabilities; (4) inference on **question-level paired differences** when comparing two models; (5) **power analysis** before you build the eval.
- Below ~300 items, don't trust plain standard errors: use **Wilson intervals** for binary outcomes and a **smooth bootstrap** for continuous scores.
- Non-determinism is a second variance source: temperature > 0 means the same prompt gives different answers. Run each item k times and either average (reducing within-item variance) or report both within- and between-item variance.

**THE FOLLOW-UP:** *"How many eval examples do you actually need?"* Expected answer shape: it depends on the effect you need to detect. Rough anchor from practice: **50–100 examples per slice** to detect a ~5-point quality shift with any confidence; hundreds to low thousands to detect 1–2 points. Then invert it: *"we need to detect a 3-point change, so n ≈ 16·p(1−p)/δ² ≈ 16·0.25/0.03² ≈ 4,400 paired items — or far fewer if we pair and the models are correlated."*

**THE TRAP:** Three, all common: (a) reporting a bare accuracy with no interval; (b) treating a 2-point difference on a 200-item eval as a regression and blocking a release; (c) computing an interval on n = number of *generations* when the items were reused, which is the clustering error from F3.

**REAL SYSTEM:** Miller (Anthropic), *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations*, arXiv:2411.00640, Nov 2024 ([HTML](https://arxiv.org/html/2411.00640v1)); the small-N companion guidance at [statsforevals.com](https://statsforevals.com/resources.html); LLM-eval CI walkthrough ([ameersaleem.substack.com](https://ameersaleem.substack.com/p/constructing-confidence-intervals)).

---

## P10. LLM-as-Judge Agreement Statistics
**Kicker:** Raw agreement percentage is inflated by chance and by class imbalance; the number that survives scrutiny is a chance-corrected one, benchmarked against human–human agreement.

- **Cohen's kappa** = `(p_o − p_e)/(1 − p_e)`: observed agreement minus chance agreement, normalised. Landis & Koch bands: 0.21–0.40 fair, 0.41–0.60 moderate, **0.61–0.80 substantial**, 0.81–1.00 almost perfect.
- Pick the right coefficient: **Cohen's** (2 raters, nominal), **Fleiss'** (>2 raters), **weighted kappa** (ordinal 1–5 scales — an off-by-one should not count the same as off-by-four), **Krippendorff's alpha** (missing data, any scale), **ICC** (continuous scores).
- **The kappa paradox**: with a heavily imbalanced label (95% "pass"), a judge agreeing 94% of the time can have kappa near zero. Always report the confusion matrix alongside kappa.
- The correct bar: **judge–human agreement ≥ human–human agreement**. If two humans agree 85%, an 85% judge is simply another annotator and you should stop apologising for it.
- Known judge biases to name, with numbers from the MT-Bench paper: **position bias** (GPT-4 only 65% consistent when the two answers are swapped; Claude-v1 23.8%, GPT-3.5 46.2%), **verbosity bias** (repetitive-list attack fooled Claude-v1 and GPT-3.5 91.3% of the time), **self-enhancement bias** (GPT-4 favours its own outputs by ~10 percentage points of win rate; Claude-v1 by ~25).

**THE FOLLOW-UP:** *"Your judge agrees with your human labels 92% of the time. Is the judge good?"* (Not yet knowable. What's the class balance? What's kappa? What's your human–human agreement on the same items? And is the 8% disagreement concentrated in the cases that matter — the borderline safety calls?)

**THE TRAP:** Reporting raw agreement on an imbalanced eval and calling it validation; using a single judge model with no position-swap control; and letting the judge model silently upgrade underneath you (judge drift), which invalidates comparisons over time.

**REAL SYSTEM:** Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (NeurIPS 2023) — GPT-4 reached **85% agreement** with humans on MT-Bench and **87%** on Chatbot Arena, against human–human agreement of **81–82%** and ~87% respectively, over ~3,000 expert votes and ~30,000 arena votes. ([arXiv:2306.05685](https://arxiv.org/html/2306.05685v4))

---

## P11. Twelve Prompt Variants Is Twelve Hypothesis Tests
**Kicker:** Picking the best of 12 prompts on your eval set is exactly the same statistical error as picking the best of 12 A/B variants — and the reported score is biased upward by construction.

- FWER with 12 independent comparisons at α = 0.05 is `1 − 0.95¹² ≈ 46%`. You will find a "winner" from noise roughly half the time.
- The reported score of the *selected* prompt is a **maximum**, and the max of noisy estimates is biased high. This is the winner's curse (C10) in the prompt-engineering loop.
- Three fixes, in order: (1) **hold out a fresh eval set** for the selected prompt — this is the only fully honest one; (2) **Holm or Benjamini–Hochberg** across the variants; (3) **max-T / bootstrap-max** correction so the CI accounts for the selection.
- Same structure applies to: hyperparameter sweeps, RAG chunking configurations, judge-prompt variants, retriever choices, and "we tried 6 models and picked the best."
- The kicker for interviews: **automated prompt optimisation makes this worse, not better** — an optimiser running 200 candidates against your dev set is a 200-fold multiplicity problem with a gradient.

**THE FOLLOW-UP:** *"You swept 12 prompts on a 200-item dev set and the best got 88% vs the baseline's 81%. What do you tell your PM?"* (That 88% is an upward-biased estimate of that prompt's true quality; you need a fresh held-out set to get an unbiased number; and with n=200 a 7-point gap has an SE around 3.5pp even before the selection bias, so the honest statement is "promising, needs confirmation on held-out data.")

**THE TRAP:** Reporting the sweep-winning score as the model's performance, then being surprised when production is 5 points lower. Also: reusing the same dev set across dozens of iterations over weeks, which is adaptive overfitting even without an explicit sweep.

**REAL FAILURE:** Recht et al., *Do ImageNet Classifiers Generalize to ImageNet?* (ICML 2019) built new test sets for CIFAR-10 and ImageNet following the original collection protocols. Accuracy dropped **3–15%** on the new sets across all models — years of community-wide adaptive tuning against a fixed public test set had inflated the reported numbers, even though relative rankings were largely preserved. ([PMLR v97](https://proceedings.mlr.press/v97/recht19a.html)); `statsforevals.com` explicitly flags that bootstrap CIs on "best prompt from a sweep" need a **max-T correction** ([statsforevals.com](https://statsforevals.com/resources.html)).

---

## P12. Paired Comparisons, Win Rates and Ranking Uncertainty
**Kicker:** A leaderboard is a point estimate of a rank, and ranks have confidence intervals too — usually wide enough that the top five models are the same model.

- **Pair whenever you can.** Same item, both models → test the per-item difference. This removes item difficulty from the variance and is often 3–10× more efficient than comparing marginal means.
- **Win rate** is a paired statistic: fraction of items where A beats B. Its SE is `sqrt(w(1−w)/n)` on the non-tie subset; report the tie rate separately because a 55% win rate with 40% ties is a different claim from 55% with 5% ties.
- **Bradley–Terry / Elo** turns pairwise outcomes into a scalar ranking. Both assume matchups are (conditionally) random and the model pool is stable — assumptions that arena leaderboards routinely violate.
- Confidence intervals on **ranks**, not just scores: build directional pairwise tests, apply Holm, and report the set of ranks a model could occupy.
- The practical consequence: "we're #3 on the leaderboard" is often indistinguishable from #1 or #6.

**THE FOLLOW-UP:** *"Model A is 1.2 points above Model B on the leaderboard. Is A better?"* (Ask: how many items, is the comparison paired, what's the SE, and is the gap larger than the *prompt-variation* noise? Then: what would change if we re-ran with a different prompt template — often more than 1.2 points.)

**THE TRAP:** Comparing two models' marginal CIs and concluding "no significant difference" when a paired test would have found one; and treating an Elo point difference as a fixed property rather than a function of the current opponent pool.

**REAL FAILURE / SYSTEM:** Neuhof & Benjamini, *Quantifying Ranking Uncertainty in LLM Benchmarks* (arXiv:2607.16259, June 2026) built rank confidence intervals over MMLU using PromptEval — **15 models, 57 subjects, 100 prompt variations** — with paired t-tests and Holm correction at α = 0.05. They found **subject-level variability substantially exceeds prompt-variant variability**, and that overlapping intervals routinely put three or more models at the same rank. ([arXiv:2607.16259](https://arxiv.org/html/2607.16259))

---

## P13. Benchmark Validity: Contamination, Label Noise, Gaming
**Kicker:** Before you argue about whether a difference is significant, check whether the benchmark measures anything at all.

- **Contamination**: the test set is in the training data. Scale AI's GSM1k — 1,000 fresh grade-school math problems built to mirror GSM8K — found accuracy drops of **up to 8%**, with Spearman r² = **0.36** between a model's probability of generating GSM8K examples and its GSM8K→GSM1k gap. Frontier models showed minimal overfitting; several families showed systematic overfitting across all sizes.
- **Label noise**: MMLU-Redux re-annotated **5,700 questions across all 57 subjects** and estimated **6.49%** of MMLU questions contain errors — with **57%** of the analysed Virology questions erroneous. A model's ceiling on that subset is the noise floor, not 100%.
- **Gaming / selective disclosure**: *The Leaderboard Illusion* (Singh, Hooker et al., arXiv:2504.20879, April 2025) documented **27 private Llama-4 variants** tested by Meta pre-release, with data-access asymmetry — Google 19.2% and OpenAI 20.4% of all arena data vs 29.7% for 83 combined open-weight models — and estimated relative gains of **up to 112%** on the arena distribution from that access. Best-of-N private submission with only the winner disclosed is the winner's curse operating at the industry level.
- **The interview point**: benchmark score = f(model, data quality, contamination, prompt, parser, judge). Attributing it entirely to the model is the error.
- Practical hygiene: canary strings, held-out private sets, freshly-authored items, and per-subset error analysis before you trust any headline number.

**THE FOLLOW-UP:** *"A vendor claims 94% on a public benchmark. What three questions do you ask before believing it?"* (1) Is the benchmark in your training data, and what's your contamination check? (2) What's the label error rate on the benchmark, and what's your score on the corrected subset? (3) How many prompt/format variants did you try, and is 94% the best or the mean?)

**THE TRAP:** Treating a public benchmark score as evidence the model will work on your task, and treating benchmark differences smaller than the label-noise rate as meaningful.

**SOURCES:** [GSM1k, arXiv:2405.00332](https://arxiv.org/abs/2405.00332); [MMLU-Redux / *Are We Done with MMLU?*, arXiv:2406.04127 (NAACL 2025)](https://arxiv.org/abs/2406.04127); [The Leaderboard Illusion, arXiv:2504.20879](https://arxiv.org/abs/2504.20879); [LMArena's response](https://lmarena.ai/blog/our-response/)

---

## P14. Power Analysis for a GenAI Online Experiment
**Kicker:** LLM features have far more per-user variance than a button colour, so the sample size you'd guess from experience is off by an order of magnitude.

- Same machinery as C3 — `n ≈ 16σ²/δ²` — but σ is much larger, because output quality varies per request, per user and per sampling seed.
- Practitioner anchor: LLM feature experiments often need **10×–100× more users** than a UI change to detect the same relative MDE.
- Reduce σ before you increase n: pair where possible, use CUPED with a pre-period engagement covariate, cap the heavy-tailed cost/latency metrics, and use a within-user design for anything comparable.
- Define the OEC before you start. For a GenAI feature this is usually *task success* or *retained usage*, not thumbs-up rate — thumbs-up has a tiny, biased response rate and is not the OEC.
- Guardrails that are specific to LLM products: p95 latency, cost per resolved task, refusal/over-refusal rate, hallucination rate on a sampled audit, escalation-to-human rate.

**THE FOLLOW-UP:** *"Design the experiment for shipping an LLM-generated summary on the product page. What's your OEC, your guardrails, your unit of randomisation, and roughly how long does it run?"* Then the sharp one: *"Your offline eval says the new prompt is better and the online test says it's flat. Which do you believe and what do you do?"* (Both can be right: the offline eval measured a dimension users don't act on, or the online test is underpowered. Check the power first, then check whether the offline metric was ever validated against an online outcome.)

**THE TRAP:** Running an LLM feature test for two weeks with the same sample-size intuition used for a checkout-flow change, getting a null, and concluding "LLMs don't help." That's an underpowered test, not a finding.

**REAL SYSTEM:** The 10×–100× sample-size guidance and the offline/online loop are documented as expected interview content for 2026 AI-engineer loops. ([vibeengines.com/handbook/llm-evals-interview](https://vibeengines.com/handbook/llm-evals-interview)); the underlying variance-reduction toolkit is the same one from P2/P7.

---
# APPENDIX A — Failure story index (48 verifiable incidents, one concept each)

Each row: the story, the single statistical concept it teaches, the number worth quoting, and a source. Rows marked ★ are already embedded in a card above; the rest are spares for card variants or a "wall of failures" page.

| # | Incident (date) | Concept | The number | Source |
|---|---|---|---|---|
| 1 ★ | Google Flu Trends (2013) | Overfitting / spurious correlation at scale | Overestimated CDC ILI in **100 of 108 weeks**; 45 terms picked from 50M; missed 2009 H1N1; lagged-CDC MAE 0.311 vs GFT 0.486 | [Science 343 (2014)](https://www.science.org/doi/10.1126/science.1248506) |
| 2 ★ | UC Berkeley admissions (1973) | Simpson's paradox | **44% men vs 35% women** admitted overall; reversed or neutral by department | [Bickel et al., Science 187:398](https://www.science.org/doi/10.1126/science.187.4175.398) |
| 3 ★ | Microsoft SRM audit (KDD 2019) | Sample ratio mismatch | **~6% of experiments** SRM; ≈1/day at 10k/yr | [KDD 2019 PDF](https://exp-platform.com/Documents/2019_KDDFabijanGupchupFuptaOmhoverVermeerDmitriev.pdf) |
| 4 ★ | MSN Carousel bot filter | SRM via log processing | Bot detector flagged engaged **treatment** users, masking a real win | same |
| 5 ★ | Skype Audio config refresh | SRM via execution | **30% of treatment sessions** lost variant IDs | same |
| 6 ★ | Microsoft Teams FRE filter | SRM via analysis trigger | Eligible users excluded from triggered analysis | same |
| 7 ★ | Optimizely peeking (2015) | Repeated significance testing | Platform FPR "**over 20% to under 5%**" after mSPRT; ~26% FPR checking every 500 visitors | [Johari, Koomen, Pekelis & Walsh, KDD 2017 PDF](http://library.usc.edu.ph/ACM/KKD%202017/pdfs/p1517.pdf); [Always Valid Inference, Operations Research 70(3) 2022](https://dl.acm.org/doi/10.1287/opre.2021.2135) |
| 8 ★ | Evan Miller's simulation | Continuous peeking | **26.1%** real FPR at nominal 5% | [evanmiller.org](https://www.evanmiller.org/how-not-to-run-an-ab-test.html) |
| 9 ★ | Airbnb price filter test | Early stopping | Significant +4% at day 7, **null** at completion | [Airbnb Eng](https://medium.com/airbnb-engineering/experiments-at-airbnb-e2db3abf39e7) |
| 10 ★ | Airbnb search redesign / IE bug | Segment analysis rescuing a null | Neutral overall; after fixing IE, **>2% boost** | same |
| 11 ★ | Google ads blindness (KDD 2015) | Long-term / learning effects | Learning half-life **~60 days**; 90-day study captures **65%**; 50% mobile ad-load cut: short-term RPM loss, long-term ≈0 | [Google Research](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43887.pdf) |
| 12 ★ | Facebook News Feed shrinkage (2019) | Winner's curse | **226 tests**; shrinkage cut MSE **44%** | [via atticusli](https://atticusli.com/replication-crisis/ab-testing-winners-curse/) |
| 13 ★ | Airbnb ERF (Lee & Shen 2018) | Winner's curse, portfolio | **20–50%** overstatement | [Airbnb ERF](https://medium.com/airbnb-engineering/experiment-reporting-framework-f3faca569e0c) |
| 14 ★ | Bing breakthrough rate | Prior odds / PPV | **1 in 500** experiments is a breakthrough → PPV **3.1%** | [Seven Rules](https://exp-platform.com/Documents/2014%20experimentersRulesOfThumb.pdf) |
| 15 ★ | Bing skewness / Revenue-per-User | CLT failure on skew | s=**17.9** → **114k users/arm** for 4.4% sensitivity; capping cut s 18→5.3 | same |
| 16 ★ | Bing abandonment experiments | Absence of evidence | Huge click shifts, abandonment p = **0.64, 0.71, 0.83, 0.92, 0.93** | same |
| 17 ★ | Bing / Amazon / Google latency | Effect size in context | Bing **+0.6% revenue per 100 ms**; Amazon **−1% sales per 100 ms** | same |
| 18 ★ | Netflix interleaving (2017) | Within-subject design efficiency | **>100× fewer users** for 95% power | [Netflix TechBlog](https://netflixtechblog.com/using-interleaving-in-online-experiments-to-accelerate-algorithm-innovation-at-netflix-a04ee392ec55) |
| 19 ★ | LinkedIn ego-clusters (2019) | SUTVA / network interference | Cluster randomisation over ego-networks | [arXiv:1903.08755](https://arxiv.org/abs/1903.08755) |
| 20 ★ | DoorDash / Lyft switchbacks | Marketplace interference | Time-slice randomisation; interference bias corrections | [DoorDash](https://careersatdoordash.com/blog/switchback-tests-and-randomized-experimentation-under-network-effects-at-doordash/), [Lyft](https://eng.lyft.com/using-marketplace-marginal-values-to-address-interference-bias-a11aff6e670f) |
| 21 ★ | Spotify sequential framework study (2023) | Sequential testing power cost | GST **90%** vs mSPRT/GAVI **72–77%** power at 0.2σ | [Spotify Eng](https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions) |
| 22 ★ | Open Science Collaboration (2015) | Replication / p-value misuse | 97% originals significant, **36%** replications; effects **halved** (r .403→.197) | [Science 349:aac4716](https://www.science.org/doi/10.1126/science.aac4716) |
| 23 ★ | Amgen preclinical cancer (2012) | PPV / base rate of true findings | **6 of 53** landmark studies reproduced | [Nature 483:531](https://www.nature.com/articles/483531a) |
| 24 ★ | Bennett's dead salmon fMRI (2009) | Multiple comparisons | ~130,000 voxels uncorrected → "activity" in a **dead fish** at p<0.001 | [poster](https://prefrontal.org/files/posters/Bennett-Salmon-2009.pdf) |
| 25 ★ | Reinhart & Rogoff (2010/2013) | Data handling + weighting errors | Corrected growth above 90% debt: **+2.2%, not −0.1%** | [PERI critique](https://peri.umass.edu/publication/does-high-public-debt-consistently-stifle-economic-growth-a-critique-of-reinhart-and-rogoff/) |
| 26 ★ | Sally Clark (1999–2003) | Prosecutor's fallacy / independence | "**1 in 73 million**" from multiplying dependent probabilities; conviction quashed 2003 | [Sally Clark](https://en.wikipedia.org/wiki/Sally_Clark) |
| 27 ★ | Literary Digest poll (1936) | Sampling frame / non-response bias | **2.4M** responses, predicted Landon 57–43; Roosevelt won 61% | [ref](https://en.wikipedia.org/wiki/The_Literary_Digest#1936_opinion_poll) |
| 28 ★ | LTCM (1998) | Fat tails / correlation instability | **$4.6bn lost in <4 months**; $3.6bn Fed-brokered recapitalisation | [Fed History](https://www.federalreservehistory.org/essays/ltcm-near-failure) |
| 29 ★ | Facebook emotional contagion (2014) | Significance ≠ magnitude | **689,003 users**; d ≈ 0.001 | [PNAS 111:8788](https://www.pnas.org/doi/10.1073/pnas.1320040111) |
| 30 ★ | Optum/Impact Pro risk algorithm (2019) | Label choice / proxy outcome bias | ~**200M people/yr**; fixing the label raised Black patients receiving extra care from **17.7% → 46.5%** | [Science 366:447](https://www.science.org/doi/10.1126/science.aax2342) |
| 31 ★ | Epic Sepsis Model (2021) | AUC vs calibration/PPV; external validation | Claimed AUC 0.76–0.83, actual **0.63**; sensitivity 33%, PPV 12%; **missed 67%** of sepsis; alerted on 18% of hospitalisations (n=38,455) | [JAMA IM / PMC8218233](https://pmc.ncbi.nlm.nih.gov/articles/PMC8218233) |
| 32 ★ | COMPAS / ProPublica (2016) | Incompatible fairness definitions | FPR ~**45% vs ~23%** by race, while calibrated within race | [ProPublica](https://www.propublica.org/article/how-we-analyzed-the-compas-recidivism-algorithm) |
| 33 ★ | Gender Shades (2018) | Disaggregated evaluation | Error **34.7%** darker-skinned women vs **0.8%** lighter-skinned men | [PMLR v81](https://proceedings.mlr.press/v81/buolamwini18a.html) |
| 34 ★ | Zech et al. chest X-ray CNN (2018) | Confounding / distribution shift | Internal AUC 0.802 → external 0.717; hospital identifiable from image at **99.95%**; prevalence 34.2% vs 1.2% | [PLOS Medicine](https://journals.plos.org/plosmedicine/article?id=10.1371%2Fjournal.pmed.1002683) |
| 35 ★ | COVID-19 imaging ML review (2021) | External validation / duplicate data | **2,212 papers** screened, 62 reviewed, **none** clinically usable | [Nature MI](https://www.nature.com/articles/s42256-021-00307-0) |
| 36 ★ | Kapoor & Narayanan leakage (2023) | Data leakage | **329 papers across 17 fields**; civil-war ML gains vanish vs logistic regression | [Patterns / arXiv:2207.07048](https://arxiv.org/abs/2207.07048) |
| 37 ★ | Recht et al. new ImageNet/CIFAR test sets (2019) | Adaptive overfitting to a public test set | Accuracy drops **3–15%** on freshly collected test sets | [PMLR v97](https://proceedings.mlr.press/v97/recht19a.html) |
| 38 ★ | Emergent abilities "mirage" (2023) | Metric choice creates the finding | Discontinuous metrics manufacture apparent phase transitions | [arXiv:2304.15004](https://arxiv.org/abs/2304.15004) |
| 39 ★ | GSM1k (Scale AI, 2024) | Benchmark contamination | Accuracy drops **up to 8%**; Spearman r² = **0.36** with memorisation probability | [arXiv:2405.00332](https://arxiv.org/abs/2405.00332) |
| 40 ★ | MMLU-Redux / *Are We Done with MMLU?* (2024/NAACL 2025) | Label noise ceiling | **6.49%** of MMLU questions erroneous; **57%** of analysed Virology items; 5,700 re-annotated | [arXiv:2406.04127](https://arxiv.org/abs/2406.04127) |
| 41 ★ | The Leaderboard Illusion (2025) | Selection on the max / best-of-N disclosure | **27 private Llama-4 variants**; Google 19.2% / OpenAI 20.4% of arena data vs 29.7% for 83 open models; up to **112%** relative gain from access | [arXiv:2504.20879](https://arxiv.org/abs/2504.20879) |
| 42 ★ | LLM benchmark rank CIs (2026) | Ranking uncertainty | 15 models × 57 subjects × 100 prompt variants; overlapping intervals put ≥3 models at the same rank | [arXiv:2607.16259](https://arxiv.org/html/2607.16259) |
| 43 ★ | MT-Bench / Chatbot Arena judge study (2023) | Judge agreement & bias | GPT-4 agreement **85%** (MT-Bench) / **87%** (Arena) vs human-human 81–82% / ~87%; position-swap consistency GPT-4 **65%**, Claude-v1 **23.8%**; self-preference **+10pp / +25pp** | [arXiv:2306.05685](https://arxiv.org/html/2306.05685v4) |
| 44 | Zillow Offers wind-down (2 Nov 2021) | Forecast error / model risk under distribution shift | Q3-21 Homes segment adjusted loss **$380.1M**; a further **$240–265M** expected on ~9,000 Q4 homes; **~2,000 jobs** (25% of staff); 9,790 homes in inventory vs 3,142 a quarter earlier. CEO Rich Barton: "the unpredictability in forecasting home prices far exceeds what we anticipated" | [GeekWire](https://www.geekwire.com/2021/zillow-shutter-home-buying-business-lay-off-2k-employees-big-real-estate-bet-falters/), [CNBC](https://www.cnbc.com/2021/11/02/zillow-shares-plunge-after-announcing-it-will-close-home-buying-business.html), [Q3-21 shareholder letter (SEC)](https://www.sec.gov/Archives/edgar/data/1617640/000161764021000085/q32021991.htm) |
| 45 | Amazon recruiting model scrapped (2018) | Biased training labels / historical base rates | Trained on 10 years of resumes; penalised "women's"; scrapped | [MIT Tech Review](https://www.technologyreview.com/2018/10/10/139858/amazon-ditched-ai-recruitment-software-because-it-was-biased-against-women/) |
| 46 | Public Health England Excel row limit (Oct 2020) | Silent data truncation before analysis | **15,841** positive COVID cases lost using .xls (65,536-row limit); contacts untraced for days | [The Register](https://www.theregister.com/2020/10/05/excel_england_coronavirus_contact_error/) |
| 47 | Ioannidis, *Why Most Published Research Findings Are False* (2005) | PPV as a function of prior, power, bias | The formal statement of the base-rate argument; most-downloaded PLoS Medicine paper | [PLoS Med 2:e124](https://journals.plos.org/plosmedicine/article?id=10.1371%2Fjournal.pmed.0020124) |
| 48 | Booking.com experimentation culture | Base rate of successful ideas | ~**90% of experiments fail** to produce the expected positive result; >1,000 concurrent experiments | [HBR podcast](https://hbr.org/podcast/2019/09/at-booking-com-innovation-means-constant-failure), [Democratizing OCE at Booking.com (KDD 2017)](https://www.researchgate.net/publication/320582817_Democratizing_online_controlled_experiments_at_Bookingcom) |

---

# APPENDIX B — The follow-up question bank

Collected verbatim or near-verbatim from 2026 question banks, company writeups and practitioner posts. Sources: [datainterview.com](https://www.datainterview.com/blog/statistics-interview-questions), [KDnuggets 24 A/B questions](https://www.kdnuggets.com/2022/09/24-ab-testing-interview-questions-data-science-interviews-crack.html), [Exponent](https://www.tryexponent.com/blog/top-statistics-data-science-interview-questions), [vibeengines LLM evals handbook](https://vibeengines.com/handbook/llm-evals-interview), [PrepVector](https://prepvector.substack.com/p/cracking-ab-testing-interviews).

**After "what is a p-value":**
- "Lift p = 0.03, CI [0.1%, 0.9%]. The PM says there's a 97% chance it's positive. Respond." *(Meta)*
- "The test isn't significant after two weeks. What do you do?"
- "Our A/B test was inconclusive and looks like an A/A test. What are the possible reasons?" *(Amplitude)*
- "In our A/B test the results were not statistically significant. Give me five reasons why." *(Amplitude)*
- "p < 0.001 and the lift is 0.02%. Ship?"

**After "how would you design an A/B test":**
- "How long would you run it, and how did you get that number?"
- "How do you verify the bucket assignment was actually random?" *(StrataScratch)*
- "What if A/B testing isn't available — how would you answer the question instead?" *(Amplitude)*
- "What development-cycle issues could contaminate your results?" *(Amplitude)*
- "Which roles on the product team should be involved, and who signs off on the OEC?"

**After "what is multiple testing":**
- "We ran 10 variants; one wins with p < 0.05. Would you make the change?" *(Emma Ding)*
- "We test 12 metrics and declare a win if any p < 0.05. What's wrong and how do you redesign it?" *(Uber)*
- "Dashboard shows a live p-value hourly and we stop when p < 0.05. Issues?" *(Netflix)*

**After "what's the effect of your winning test":**
- "The test showed 1% improvement. Should you expect the same after launch?" *(Emma Ding)*
- "Why might a winning test's effect decline after full launch?" *(Emma Ding)*
- "The desired metric increased but impressions decreased. How do you decide?" *(Emma Ding)*
- "Overall lift is positive but negative for a key segment. What do you do?" *(Spotify)*

**After "what test would you use":**
- "Bookings are highly skewed with a spike at zero and the team wants a t-test. Your approach?" *(Airbnb)*
- "How do you handle outliers in customer spend?" *(Microsoft)*
- "Your regression has heteroskedastic residuals. Does that bias the coefficients?" *(Spotify)*
- "Two features correlate at 0.95 with opposite-signed significant coefficients. Explain." *(Meta)*
- "You control for number of enquiries when estimating the effect of Instant Book. Is that OK?" *(Airbnb)*

**After "what is Bayes' theorem":**
- "Construct a prior for a new city launch." *(Uber)*
- "Give me a Bayesian upper bound on a rare event rate." *(Google)*
- "Compare Model A and Model B CTR the Bayesian way." *(Netflix)*
- "Build a hierarchical model for sparse listing data." *(Airbnb)*

**After "how do you evaluate an LLM" (2026 core):**
- "How many examples do you actually need?" → the CI arithmetic
- "You got 82% on 50 prompts. What's your confidence interval?"
- "Model A 82%, Model B 79% on the same 500 items, CIs overlap. Is A better?" → paired test
- "How do you validate an LLM judge?" → kappa vs human-human agreement
- "What are the known biases of LLM judges?" → position, verbosity, self-preference, sycophancy, format
- "You swept 12 prompts and the best got 88% vs baseline 81%. What do you report?"
- "How do you set a regression-test threshold that doesn't fire on noise?" → bootstrap the golden set, gate on the CI
- "How do you handle non-determinism at temperature > 0?"
- "Your offline eval says better, your online A/B says flat. Which do you believe?"
- "How many users do you need for an online LLM feature test vs a UI change?" → 10×–100×

**The generic killers (asked at the end of almost any stats round):**
- "What would make you distrust this result?"
- "What's the first thing you check when a result looks too good?"
- "What assumption in your analysis is most likely to be wrong?"

---

# APPENDIX C — The trap list: specific wrong things candidates say

Not "people struggle with Bayes." These are sentences that get said out loud and cost the loop.

1. "The p-value is the probability the null hypothesis is true." / "…the probability I'm wrong."
2. "p = 0.06 is trending toward significance."
3. "We failed to reject, so there's no effect." (absence of evidence)
4. "There's a 95% probability the true value lies in this confidence interval." (that's a credible interval)
5. "The confidence intervals overlap, so the models are the same." (must test the paired difference)
6. "n > 30 so the CLT applies." (ignores skew; Bing needs 114k for revenue/user)
7. "I have 2 million rows, so I have plenty of power." (you have 40k users)
8. "We only peeked twice, that's fine." (already ~2× the α)
9. "Bayesian A/B testing solves the peeking problem." (it changes the interpretation, not the operating characteristics of your stopping rule)
10. "Beta(1,1) is an uninformative prior." (uniform on p is informative on the odds scale)
11. "I'll use Mann–Whitney because the data aren't normal," then reporting a mean lift.
12. "Shapiro–Wilk says non-normal so the t-test is invalid." (with n=100k it always rejects; you need normality of the *sampling distribution*)
13. "I used Student's t-test." (Welch should be the default)
14. "More control variables reduce bias." (bad controls, mediators, colliders)
15. "I controlled for it in the regression, so it's causal."
16. "AUC is 0.97 so the model is great," on 0.1% prevalence data.
17. Reporting AUC on a re-balanced *test* set.
18. "I used cross-validation so there's no leakage." (preprocessing fitted outside the fold)
19. "Zero failures in 500 runs, so the failure rate is 0%." (rule of three: up to 0.6%)
20. "The lift is 0.4% off from 50/50, that's fine." (chi-square SRM at scale says otherwise)
21. Finding an SRM, dropping the affected users, and proceeding.
22. "We'll adjust for the SRM." (you can't; the bias direction is unknown)
23. "The effect declined after launch because of novelty." (without ruling out winner's curse, population shift, or interference)
24. "We tried 12 prompts and the best got 88%." (reporting a selected max as an unbiased estimate)
25. "The judge agrees with humans 92% of the time." (no kappa, no class balance, no human–human baseline)
26. "MMLU is 89% so it'll work for our task." (contamination, 6.5% label noise, task mismatch)
27. "We're #3 on the leaderboard." (rank has a CI; #1–#6 may be indistinguishable)
28. "We ran it for two weeks and it was flat, so LLMs don't help here." (underpowered by 10–100×)
29. "The drift monitor fires every day so we turned it off." (p-value alarm at scale; should be PSI/effect size)
30. Inventing the OEC after seeing the results.
31. "Statistically significant" used as a synonym for "important" — and the mirror error, dismissing a 0.3% lift worth $40M.
32. Answering "how do you determine sample size?" with the lift you hope for instead of the smallest lift that matters.
33. Quoting sample size without saying **per arm**, and without converting to whole weeks.
34. Saying "network effects" without naming a design, the direction of the bias, or the power cost.
35. Describing CUPED as a bias correction rather than variance reduction.
36. Using an in-experiment covariate in CUPED.
37. Computing `sum(clicks)/sum(impressions)` and z-testing it with n = impressions.
38. Bootstrapping rows in clustered data.
39. Reporting the mean of log-transformed revenue as a percentage revenue lift.
40. Never mentioning A/A tests, pre-registration, or guardrails in an experiment-design answer.

---

# APPENDIX D — Card build notes

- **Tier balance shipped here:** Foundation 10, Core 13, Advanced 11, In Production 14 = **48 cards**. Trim Foundation F7/F10 and Advanced A11 first if you need to land at 45; they're the least likely to be asked directly.
- **Every card follows:** title → kicker (tension, never a definition) → 3–6 substance bullets → THE FOLLOW-UP → THE TRAP → REAL FAILURE with numbers + URL.
- **Highest-leverage cards for a 2026 loop, in order:** C1 (p-value follow-up), C3 (power/MDE arithmetic), P9 (eval CIs), C4+C5 (peeking/sequential), P1 (SRM), C6/P11 (multiplicity), P2 (CUPED), P10 (judge agreement), C10 (winner's curse), P3 (randomisation unit).
- **The three numbers to over-learn:** `n ≈ 16σ²/δ²`, `SE = sqrt(p(1−p)/n)`, `rule of three = 3/n`. Every quantitative follow-up in the bank is reachable from these plus arithmetic.
- **Currency check:** all LLM-eval material dates from Nov 2024 (Anthropic error bars) through June 2026 (ranking-uncertainty CIs); experimentation material spans the KDD 2013–2019 canon plus 2023–2026 platform docs. Nothing here is a 2019 listicle.
