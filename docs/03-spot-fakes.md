# Chapter 3 · Fakes, shills, and affiliate funnels

Nobody in 2026 reads reviews naive anymore, and mostly that's healthy skepticism. But there's a difference between *dismissing* reviews wholesale (which throws away good information) and *auditing* them (which keeps the good and tosses the bought). This chapter is the audit. It's two short routines: one for review sections, one for "best of" list sites.

## Part one: the review-section audit

Six tells that reviews in a section aren't what they seem:

1. **The avalanche.** A product launched this month but has two hundred reviews dated within ten days. Real adoption takes longer; bought reviews launch on schedule.
2. **The twin reviews.** Same sentence structure ("This exceeded all my expectations for the price!") across reviews, or across *different products and brands*. Real strangers write alike only by accident.
3. **The generous stranger.** "I received this product free in exchange for my honest review." Honest-ish, sure, but gratitude is a filter that bends taste. Treat these as ads wearing an honest hat.
4. **The barbell.** All five stars and one stars, almost nothing in between. Real products cluster with a bell shape; barbell distributions often mean review wars between camps (or a coordinated defense against them).
5. **The mega-reviewer.** A single account has posted forty reviews this week, all in the same category, all positive.
6. **The brochure photo.** Review photos that look like press shots, at identical angles across reviews, are usually studio stock provided by the seller.

None of these are courtroom proof on their own. One avalanche means curiosity; an avalanche with twins and brochure photos means walking away.

And a trick that works upside down: **the middle is the truth.** Average reviews (2 to 4 stars) tend to be the most informative, because the writer has no agenda in either direction and often details one specific dealbreaker. "Four stars: perfect bed, but it squeaks over 30 degrees outside" is worth five glowing essays.

## Part two: the "best of" site audit

"Best blender for 2026" ranking sites are a mixed bag: some are genuinely tested by humans with lab gear; many are content farms where the "rankings" quietly match whatever pays the highest affiliate commission. You don't have to swear off them; you just have to know which kind you're reading. The two-minute incentive check:

- Is there a **disclosure page** you can find in under a minute (look for "affiliate disclosure" or "how we test")? FTC rules in the US require disclosure of paid placement; honest sites make it easy, nervous sites bury it.
- Are there **their-own photos**? Hands, crumbs, scratched test benches, the reviewer's kid in the background? Real testing leaks real mess. Stock photos of the product are what content farms use.
- Does the **actual wording** recommend on merit within a category, or does every "top pick" conveniently link to one marketplace with the same tracking suffix? A URL ending in `?tag=` or similar is an affiliate link; that fact alone doesn't invalidate the review, but the ranking and the money now share an address.
- Is it **up to date**? A page saying "best for 2026" with no review dated this year is a keyword wearing a costume.

Also worth knowing: the biggest "best" lists are written by staff who sometimes never touched the product, and some of the best reviewers are individuals with zero advertising. The incentive check is how you tell them apart, and AI can help: paste a "best of" page's text into a chat and ask it to *strip every recommendation down to its factual skeleton* ("claims a 400-watt motor, calls it quiet, says 5-year warranty"). Facts can be verified in [Chapter 4](spec-sheets.html) style. Vibes cannot.

## Part three: let the AI hunt patterns

Same collecting trick as the last chapter, one new prompt. Paste your review dump, sorted oldest first:

```
Below are reviews for {product}, sorted oldest first. I suspect
some may be fake or coordinated. Look for:

1. Near-duplicate or boilerplate sentences shared across
   reviews. Quote each repeating phrase and list which reviews
   share it.
2. Review bursts: dates where many reviews appear close
   together, especially ones that read promotional.
3. Reviews that praise the seller, shipping, or brand rather
   than the product's actual behavior.

Do not tell me whether to buy the product. Only report your
findings, with quotes.

REVIEWS:
[paste reviews here]
```

AI is genuinely good at this kind of copy-paste pattern matching: it never gets bored and never flatters. That said, keep the verdict in your own head: the model can find the twins, but you decide what the twins mean.

One last calibration note, so this chapter doesn't turn you cynical: most reviews are real. Most reviewers wanted neither money nor products, just a place to vent about a rattling freezer or to say thank you for a mattress that fixed a bad back. The audit exists so that the honest 80% (the signal) isn't drowned out by the paid 20%.

Next: [Chapter 4 · Spec sheets, translated](spec-sheets.html)
