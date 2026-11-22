# Fore The Money Requirements

These notes capture the current product decisions and open questions; they do not
imply that the behavior is implemented. Resolve open questions before turning
them into implementation-ready stories.

## Product scope

- A season-long PGA Tour golf pool for friends, with a possible public release
  later.
- A person can join multiple leagues, with separate picks and settings in each.
  The existing database calls a league a pool.
- Cash prizes are handled outside the app; payment features are not planned for
  now. Review legal considerations before supporting public real-money pools.

## Functional Requirements

### Tournaments and tiers

- A league admin selects which tournaments count and sets the cut points for
  four quarters. The app may recommend an even split, but the admin makes the
  final selection. Admins may change inclusion and quarter assignments only
  for tournaments that have not started.
- Take the betting-odds snapshot Tuesday at 8:00 a.m. Central Time, accounting
  for daylight saving time. If a complete usable snapshot is unavailable,
  flag the issue and wait rather than publish tiers from incomplete data.
- There are six tiers. Tier 1 contains the 10 golfers with the shortest odds;
  tiers 2 through 5 each contain the next 10; tier 6 contains the rest of the
  field. Use this standard arrangement for fields of at least 50 golfers.
  With exactly 50 golfers, tier 6 is empty and scores zero. For fields with
  fewer than 50 golfers, each league admin manually assigns the available
  golfers to six tiers for their league.
- Break equal odds at tier boundaries using world golf ranking, sorting ranked
  golfers ahead of unranked golfers. Use a stable golfer identifier if rankings
  cannot separate them.
- If a golfer enters the field after tiers are published, update the tiers and
  send push notifications to league admins and players. Compare the entrant's
  current odds with the original snapshot odds without refreshing the other
  golfers' odds. Clear a pick whose golfer moves to a different tier, so the
  member can pick again for that tier. If the picked golfer has already teed
  off, keep the original pick valid and scoring instead.
- Remove a golfer who withdraws before the tournament starts without moving
  the remaining golfers between tiers, even if a tier has fewer than 10.

### Picks and lock

- A league member picks one golfer from each tier for each counted tournament.
- Picks can be changed freely until a single pool-wide lock at the tournament's
  first tee shot, except for the late tier-change replacement described below.
  A golfer can be picked again in subsequent weeks.
- If a tier change clears a member's pick after 5:00 p.m. Central Time on the
  day before the tournament starts, the affected member can pick a replacement
  until the replacement golfer's tee time instead of the tournament-wide lock.
  A replacement chosen after the tournament-wide lock is final immediately.
- A golfer who withdraws before the tournament's first tee shot can be replaced
  by resubmitting before the lock. After the tournament starts, a withdrawal
  scores zero even if that golfer has not yet teed off.
- A member with no saved picks scores zero for that tournament; picks do not
  carry forward. Saved partial picks score normally, with an empty tier worth
  zero.

### Scoring and standings

- A member's tournament score is the combined earnings of their saved golfers.
  A missed cut or withdrawal after the first tee shot scores zero for that
  golfer. No weighting is applied: higher purses at majors and signature events
  intentionally have a larger effect.
- Four quarter winners and one season winner are determined by earnings from
  the league's counted tournaments. Quarter totals reset each quarter; season
  totals continue accumulating. The same member may win both. Members tied
  on earnings share the quarter or season title.
- Use official prize money from Slash Golf via RapidAPI. Earnings are usually
  populated a few hours after a tournament and can change through Monday, after
  which results are expected to be final. Later corrections update standings
  and trigger push notifications to league admins and players.
- Calculate projected live earnings from leaderboard positions and the purse;
  show the most up-to-date available figures. How to label projected,
  unofficial, and official figures remains open.

### Parked: late submission pass

- A possible one-time pass, parked outside version one, would allow one late
  submission per member per season. Only golfers who have not yet teed off
  could score; already-started slots would score zero or remain blank.
- After the pass is used, a missed week would score zero. Its detailed behavior
  and whether the API provides the necessary individual tee times are unresolved.

## Non-Functional Requirements

- Start with free data access where feasible; investigate alternatives or paid
  limits if usage grows. Confirm the reliability and availability of required
  odds, leaderboard, earnings, and tee-time data.
- The current backend uses FastAPI, Pydantic, SQLAlchemy, PostgreSQL, and
  Alembic. Confirm the broader stack as the product design develops.

## Open decisions and investigation

- Find a suitable odds source: Slash Golf does not appear to provide the
  required odds. Confirm coverage, cost, and availability of snapshots.
- Define snapshot recovery and how other field changes affect tiers.
- Decide the detailed late-pass rules if the pass is added later.
- Define how live projections and revised official results are presented and
  when results become final.
- Determine how admins manage counted tournaments and quarter boundaries
  without altering tournaments that have started.
- Resolve the data-model gaps: persisted tier snapshots, league tournament
  selection, quarter and score breakdowns, pick lock and swap history, tier
  validation, and late-pass tracking if included. Review earnings and year
  types for their expected ranges and API compatibility.
- Existing models contain per-golfer leaderboard tee times, but their presence
  does not establish that the API reliably supplies them.
