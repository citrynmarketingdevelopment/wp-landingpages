# Fill-In Notes — `pwc/reviews.html`

The Reviews page is built and styled, and the 9 review cards are filled in with real Google
reviews you provided (Lei Shapiro, Hat Capper, Hilarie Schmalz, Marie Belknap, Elizabeth Winzer,
Barb Beach, Samantha Black, shayna stolte, Lauren Williams — newest to oldest). Review names are
reproduced exactly as capitalized on Google (a couple are lowercase by the reviewer's own choice),
and typos in the original text (e.g. "Psychiatric Wellness Centrr") were kept verbatim rather than
corrected, per the page's own claim that reviews are shown "as written."

Four **placeholder tokens** remain — business facts that only you can supply. Nothing on this page
should go live until every `{{TOKEN}}` is replaced — a token left in place will render literally
as `{{RATING}}` on the page.

Find them all:

```bash
grep -o '{{[A-Z0-9_]*}}' pwc/reviews.html | sort -u
```

## Why hand-coded cards and not a live widget

GitPress sanitizes fetched GitHub fragments and strips third-party `<script>` tags, so an
Elfsight/Trustindex JS embed pasted into this file would not run. Hand-coded cards render
reliably, load instantly, and the text is crawlable for SEO. The trade-off is that they are a
**snapshot** — they do not update when a new Google review comes in. The "Read All Reviews on
Google" buttons cover that by sending people to the live profile.

## Tokens still needed

| Token | What to put there |
|---|---|
| `{{RATING}}` | Your live Google Business Profile rating, e.g. `4.9` |
| `{{REVIEW_COUNT}}` | Your live Google review count, e.g. `63` |
| `{{GOOGLE_PROFILE_URL}}` | Link to your Google Business Profile reviews tab |
| `{{GOOGLE_REVIEW_URL}}` | Your "write a review" short link (Google Business Profile → Ask for reviews → copy link, format `https://g.page/r/…/review`) |

There are 9 review card slots (`<!-- REVIEW 1 -->` … `<!-- REVIEW 9 -->`), already filled in. Use
fewer or more if the review set changes later:

- **Fewer reviews:** delete the whole `<div class="rev card"> … </div>` block for the slots you
  don't need. The grid reflows on its own — no CSS change required.
- **More reviews:** copy an entire `<div class="rev card"> … </div>` block, paste it before the
  closing `</div>` of `.rev-grid`. Multiples of 3 look best on desktop.
- Dates were converted from Google's relative timestamps ("26 weeks ago") to `Month Year` as of
  2026-07-30, the day this page was built. If you swap in fresher reviews later, recompute the
  month from the current date rather than reusing these.
- Skipped: Sandy Randel, Cindy Barry, Coulter Marshall (no review text), and Dominic ("The
  psychiatrist was nice" — too thin to be a useful card). James Dent and Rodrigo Uribe were left
  out only to keep the grid at 9; both have usable full text if you want to swap one in later.

## Star ratings

Every card is hard-coded to 5 stars (five `<svg>` elements inside `.stars`). For a 4-star review,
delete one `<svg>` and change `aria-label="5 out of 5 stars"` to `aria-label="4 out of 5 stars"`.
The hero panel's star row is separate and does the same thing.

## Rules to keep the page honest

- Only publish text that was **actually written by a patient on Google**. Do not write filler
  reviews to fill the grid — the page states in three places that these are real Google reviews,
  and the FAQ says outright that nothing is offered in exchange for one. Fewer real cards beats
  six invented ones.
- `{{RATING}}` and `{{REVIEW_COUNT}}` are a claim about your business. Re-check them against the
  live profile whenever you touch this page.
- The `.source-note` line under the grid and the FAQ ("Do you offer anything in exchange for a
  review?", "Can a review tell me whether treatment will work for me?") are there deliberately —
  healthcare testimonial pages draw scrutiny. Keep them.
- HIPAA runs one direction: patients may disclose their own care publicly, the practice may not.
  Do not add any clinical detail to a card that the reviewer did not write themselves, and do not
  respond publicly with anything that confirms treatment specifics.

## Keeping it current

Re-check the page ~2× a year: refresh `{{RATING}}` / `{{REVIEW_COUNT}}`, swap in newer reviews,
bump the `<!-- webhook retrigger YYYY-MM-DD -->` marker on line 1, push, and confirm the new
marker appears in the live page source before debugging anything.
