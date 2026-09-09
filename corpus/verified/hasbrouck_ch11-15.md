# Per-Chapter Verification — Hasbrouck *Empirical Market Microstructure*, Ch 11–15

**Verifier:** subagent · **Source text:** `/tmp/atlas_extract/hasbrouck.txt` (line refs below)
**Extraction checked:** `market_microstructure.md` §10–§13 (Hasbrouck Part 1) and Atlas mappings
**Method:** full text read of Ch 11 (lines ~4913–5415), Ch 12 (~5416–5946), Ch 13 (~5947–6461), Ch 14 (~6462–6891), Ch 15 (~6892–7485). Text-based; no math recomputation beyond algebra tracing. **Sources not modified.**

## Overall verdict
Extraction for Ch 11–15 is **accurate — no factual or formulaic errors found.** Every formula, result, and attribution I checked in the text matches the extraction. Discrepancies are minor *omissions* (details the extraction chose not to carry), none of which are wrong. Detail below per chapter.

---

## Ch 11 — Dealers and Their Inventories  (extraction §10: ✅ correct)

Verified correct:
- **Garman (1976):** asynchronous Poisson buyer/seller arrivals; profit `π(Bid,Ask) = (Ask−Bid)·λBuy(Ask) = (Ask−Bid)·λSell(Bid)`; if `λBuy(Ask)=λSell(Bid)` inventory is a zero-drift random walk (cash positive-drift) ⇒ ruin with probability 1, expected ruin time ~days; remedy = price inventory adjustment (text 4952–5015). ✓
- **Amihud–Mendelson (1980):** monopolistic dealer, inventory bounds (credit constraints), preferred inventory level; bid/ask **monotone decreasing in inventory**; positive spread; spread increasing in distance from preferred position; quotes not symmetric about true value; inventory price effects **transient** (text 5026–5057). ✓
- **Stoll (1978) risk aversion, CARA-normal:** `U(W)=−e^{−αW}`; CE `= µW − ασW²/2`; bid `B = µx − (2n+1)ασx²/2` (11.2); optimal holdings `n* = (µX−P)/(ασX²)`; at optimum `B = P − ασX²/2` (text 5110–5144). ✓
- **Multisecurity:** `B1 = µ1 − (ασ1/2)[(1+2n1)σ1 + 2ρn2σ2]` (11.3) — positive correlation ⇒ less aggressive quoting; **but at the optimum ρ drops out** under CARA (text 5147–5168). ✓
- **Empirics:** NYSE specialists (Hasbrouck–Sofianos 1993; Madhavan–Smidt 1991/93; Madhavan–Sofianos 1998) mean-revert, "go home flat" (small overnight positions), no drift; most quote dynamics attributable to **trades**, inventories contribute little explanatory power (text 5180–5348). ✓
- **Info vs inventory effects:** information effects permanent, inventory effects temporary (Hasbrouck 1988) (text 5332–5335). ✓
- **Empirical techniques:** unit-root tests (roots of `φ(z)=0`, |φ1|<1); differencing/overdifferencing → noninvertible MA estimated by **Kalman-filter ML**; VAR with price changes, signed orders, specialist inventory (text 5249–5348). ✓

Minor omissions (not errors): text also notes levered inventories + credit as the real ruin channel (Brunnermeier–Pedersen 2005), Madhavan–Smidt (1991) joint inventory+adverse-selection model, Yao (1997) selective/nonpublic quoting, Madhavan–Sofianos (1998) specialist participation (last-mover). None contradict the extraction.

---

## Ch 12 — Limit Order Markets  (extraction §11: ✅ correct)

Verified correct:
- **Framing:** limit order = "dealer quote by another name," exposed to adverse selection + must recover noninformational costs; essence of LOM = make/take roles blurred, liquidity supplied by customers; a customer's limit order need not satisfy zero-expected-profit (text 5427–5447). ✓
- **Order choice (CMSW 1981; Angel 1994; Harris 1998):** CARA-normal; `EULimit(L)=PrHit(L)·EUHit(L)+[1−PrHit(L)]EUBase`; exponential execution prob `PrHit(L)=1−exp[−λ(L−θ)]`; **gravitational pull** — switch point (A=1.17) above optimal limit price (L=0.75), condition `lim_{L→A} PrHit(L)` bounded away from 1, explains finite spread with continuous prices (text 5497–5595). ✓
- **Parlour (1998):** dynamic equilibrium, backward recursion from T; `B<V<A` fixed; depth builds from empty book then **drops near close**; predictions (i) ↑ bid-side depth ↓ buyer limit-order use (same-side), (ii) ↑ offer-side depth ↑ buyer limit-order use (opposite-side); symmetric for sells (text 5619–5786). ✓
- **Foucault (1999):** random stopping time (prob 1−ρ per period), value innovations `εt=±σ`, reservation `Rt=vt+yt`; one-shot; **pick-off risk / winner's curse** on `εt+1=−σ`; comparative statics: fundamental risk σ ↑ ⇒ higher pick-off risk ⇒ limit prices fade, **spread widens**, order mix shifts toward limit orders (fewer execute) — a cross-sectional prediction (text 5797–5863). ✓
- **Empirical event models:** multinomial logit `Pr(Yt=i)/Pr(Yt=0)=exp[αi+Ztβi]` (12.1); ordered logit `logit(Pr(Yt≤i))=αi+Ztβ` (12.2); consistent findings — **wide spread → favor limit orders; same-side depth → favor market orders**; opposite-side-depth support "less clear" (text 5866–5941). ✓

Minor omissions: initial studies named (Tokyo SE Lehmann–Modest, Hamao–Hasbrouck; Paris Bourse Biais–Hillion–Spatt); the fact that the same-side-depth prediction is supported by Renaldo, Ellul, Hasbrouck–Saar. Not errors.

---

## Ch 13 — Depth  (extraction §12: ✅ correct)

Verified correct:
- **Stylized fact:** posted supply/demand schedules too steep vs dynamic price-revision functions (Sandas 2001, OMX) — book schedules steepest (mean > median, outliers at low depth), dynamic-revision lines shallowest; "backfilling"/depth reappearing at better prices; implies splitting large orders is cheaper (text 5958–6003). ✓
- **Glosten (1989, 1994)** three regimes: competitive dealer, limit order book, monopolistic dealer (text 6006–6011). ✓
- **Competitive dealer:** price = `E[value|trade]`; order splitting ruled out (customer discloses full size, gains nothing); market fails if customer informational advantage too high (text 6028–6052). ✓
- **Limit order book:** discriminating executions (like a discriminating monopolist); marginal limit order priced at **upper-tail conditional expectation** `P(q)=E[X|m≥m(q)]` because it also executes against larger orders; even an infinitesimal order incurs positive spread (`lim P(q)>µX`) vs competitive dealer `lim P(q)=µX` (text 6055–6310). ✓
- **Monopolistic dealer:** rents; **cross-subsidization** can keep market open where competitive dealer fails (text 6088–6110). ✓
- **Formulas — all match:** customer FOC `µX − (q+n)ρσX² − R′(q) = 0` (13.1); signal `S=X+ε`; competitive schedule `P(q)=k0+k1q` with `k0=µX`, `k1 = ρσX²σε²/(ρ²σn²σε⁴ − σX²σε²)` (13.5); upward-slope/market-failure condition `σε²(ρ²σn²σε²−1) − σX² > 0`; truncated-normal tail expectation `E[X|X≥X̄]=µ+σφ(·)/(1−Φ(·))` (13.6) (text 6141–6272). ✓
- **Sandas dynamic version:** exponential order-size distribution `f(b)=e^{−bλ}/λ`; break-even conditions Q1,Q2,… determine book depth; break-even-based schedules closer to observed, dynamic-revision α estimates too shallow; joint restrictions rejected (text 6349–6414). ✓
- **Depth improvement / pennying (Seppi 1997; Rock 1990):** hybrid market, dealer last-mover advantage, depth improvement (Bacidore 2002), eighthing→pennying; can also produce price improvement (text 6423–6461). ✓

Minor omissions: exact sign of `∂k1/∂σX²>0, ∂k1/∂σε²,∂k1/∂σn²,∂k1/∂ρ<0`; Pareto note that the dealer's loss region in the monopolist case enforces separation. Not errors.

---

## Ch 14 — Trading Costs: Retrospective and Comparative  (extraction §13: ✅ correct)

Verified correct:
- **Implementation shortfall (Perold 1988):** `IS = (v−n1)′π1 = (n1−n0)′(p−π0) + (v−n1)′(π1−π0)` = **Execution cost + Opportunity cost** (14.1); n0=actual initial, v=paper/desired, n1=actual final, π0/π1 initial/terminal benchmark prices; opportunity cost ≈ tracking error; **execution costs are zero-sum across users sharing benchmark π0** (text 6539–6642). ✓ Matches extraction exactly.
- **Effective cost** = `pt − mt` (pretrade BAM); **realized cost** = `pt − mt+5`; `pt−mt = (pt−mt+5) + (mt+5−mt)` (14.2); `mt+5−mt` = price-impact estimate; SEC Rule 605 (formerly 11ac1-5, "dash five") (text 6698–6716). ✓
- **VWAP:** day interval, easier (no time matching), used to evaluate brokers; objections — orders differ in difficulty; if you account for a large share of daily volume the avg price ≈ VWAP regardless of handling (order-size-dependence); **gamable** (Harris 2003) (text 6718–6730). ✓
- Applications: Plexus/SEI data studies (Keim–Madhavan 95% completion; Chan–Lakonishok), trade-based `|p−BAM|` cost, selection effects (Madhavan–Cheng 1997; Bessembinder 2004), Harris–Hasbrouck (1996) imputation for canceled orders. ✓

Minor omissions: the tournament/aggregate-IS illustration (lucky-first-trader, misleading aggregate $991) and the qualification that opportunity cost may be negative / is measured relative to possibly-revised desired portfolio. Not errors.

---

## Ch 15 — Prospective Trading Costs and Execution Strategies  (extraction §13: ✅ correct)

Verified correct:
- **Order splitting / timing (Bertsimas–Lo 1998; Almgren–Chriss 2000; Almgren 2003):** permanent impact `mt = mt−1 + µ + λst + εt` (15.1); temporary impact `pt = mt + γst` (15.2); constraint `s̄=Σst`; **optimal level `st* = s̄/T` when µ=0**; with µ≠0, `st* = s̄/T + [(T+1)−2t]/(2(2γ+λ))·µ` (15.4) — linear acceleration with drift (buy), inversely related to γ,λ (text 6916–6996). ✓
- **Slowly-decaying temporary effects:** nonstochastic — state `At = Σθ^i·s_{t−i} + θ^t A0`, `pt = mt + γAt + εt` ⇒ **U-shaped strategies**; stochastic — `At = st + θAt−1 + ut`, solved by **dynamic programming** (value fn `Vt(mt−1,wt,At−1)`) (text 7006–7107). ✓ Matches extraction ("U-shaped strategies with slowly-decaying temporary impact; dynamic programming with stochastic temporary effects").
- **Order placement (Harris 1998; Handa–Schwartz 1996; Lo–MacKinlay–Zhang 2002):** diffusion-barrier model `dpt=µdt+σdz`; limit order executes when price hits barrier; value-function dynamic programming; **more aggressive as deadline approaches**; positive drift ⇒ more aggressive prices, ↑ volatility ⇒ less aggressive (higher execution prob); **µ=0 ⇒ no advantage to limit order** (market order immediately optimal; µ>0 strictly so; µ<0 no interior optimum) (text 7130–7377). ✓
- **Duration analysis:** exponential/Poisson; diffusion-barrier = first-passage model — Lo et al. find it **underestimates** times to execution (too optimistic), generalized gamma better; **censoring** critical (vast majority canceled; Hasbrouck–Saar: only ~13% of submitted limit orders executed) (text 7380–7441). ✓

Minor omissions: the exact recursive value-function (15.14–15.17) and the reflection-principle martingale argument underpinning the µ=0 result; the manipulability caveat (Exercise 15.1 initial-sale can be viewed as manipulative). Not errors.

---

## Atlas-mapping checks (Part 3 rows touching Ch 11–15)
- **Pillar 06 inventory-management-and-quote-skewing** ← Ch 11: correct (Garman, Amihud–Mendelson, Ho–Stoll, Stoll, `m_t=µ_t−ρσεz_t` is from Foucault, correctly sourced there). ✓
- **Pillar 02 execution-algorithms-vwap-twap-pov** ← Ch 14: correct. **optimal-execution-and-almgren-chriss** ← Ch 15: correct (`s_t*=s̄/T`, permanent/temporary impact, DP, U-shaped). **queue-position-and-fill-probability** ← Ch 15: correct (PrHit, diffusion-barrier, duration). ✓
- **Reading path items 8 (Ch 12–15) and 6 (Ch 11):** consistent with verified content. ✓

## Corrections to record
**No errors requiring correction.** The only flagged items are deliberate scope omissions, listed per chapter above. If desired, the extraction could be enriched with: Ch 14 aggregate-IS/tournament illustration; Ch 15 zero-drift no-limit-order-advantage result and the ~13%-execution censoring statistic; Ch 13 ∂k1 sign conditions. None are inaccuracies in the current text.

## Files
- **Created:** `/tmp/verified/hasbrouck_ch11-15.md` (this report).
- **Modified:** none (sources untouched, per instruction).
