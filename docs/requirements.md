# Fore The Money Requirements

These notes capture the current product decisions and open questions; they do not
imply that the behavior is implemented. Resolve open questions before turning
them into implementation-ready stories.

## Product scope

- A season-long PGA Tour golf pool for friends, with a possible public release
  later.
- A person can join multiple leagues, with separate picks and settings in each.
  The existing database calls a league a pool.
- Leagues are private in the friends-first version: members join through a
  unique invitation link or code created by the league admin.
- The league creator is the owner and initial admin. Admin rights may be
  granted to members. Only the owner may delete the league or transfer ownership.
- An invitation link or code is reusable until an admin disables or replaces
  it or the first counted tournament of the season tees off. No new members
  join after the season begins.
- If an admin removes a member, preserve the member's historical picks and
  standings but mark them inactive so they cannot submit new picks.
- Cash prizes are handled outside the app; payment features are not planned for
  now. Review legal considerations before supporting public real-money pools.

## Functional Requirements

### Tournaments and tiers

- A league admin selects which tournaments count and sets the cut points for
  four quarters. The app may recommend an even split, but the admin makes the
  final selection. Admins may change inclusion and quarter assignments only
  for tournaments that have not started, including mid-season changes. Notify
  all league members when an admin changes the tournament schedule or quarter
  assignment.
- The admin defines the four quarters by choosing the tournament where each
  quarter begins and reviews the resulting quarter ranges before the season
  begins. Each quarter must contain at least one counted tournament.
- When recommended, the app divides the admin-selected counted tournaments
  into four consecutive groups as evenly as possible, adding any remainder
  to the earlier groups in tournament order.
- Take the betting-odds snapshot Tuesday at 8:00 a.m. Central Time, accounting
  for daylight saving time. If a complete usable snapshot is unavailable,
  keep retrying and publish tiers from the first complete odds data received,
  notifying league admins and members. If complete data does not arrive before
  the tournament starts, skip that tournament for the pool.
- There are six tiers. Tier 1 contains the 10 golfers with the shortest odds;
  tiers 2 through 5 each contain the next 10; tier 6 contains the rest of the
  field. Use this standard arrangement for fields of at least 50 golfers.
  With exactly 50 golfers, tier 6 is empty and scores zero. For fields with
  fewer than 50 golfers, each league admin manually assigns the available
  golfers to six tiers for their league before assignments are published and
  picks open. Admins choose the tier boundaries, but golfers remain in odds
  order, with the normal tie-breakers applied.
- Break equal odds at tier boundaries using world golf ranking, sorting ranked
  golfers ahead of unranked golfers. Use a stable golfer identifier if rankings
  cannot separate them.
- After publication, ignore changes in existing golfers' odds; retain their
  snapshot-based order. Late field entrants are handled separately below.
- If a golfer enters the field after tiers are published, update the tiers and
  send push notifications to league admins and players. Compare the entrant's
  current odds with the original snapshot odds without refreshing the other
  golfers' odds. Clear a pick whose golfer moves to a different tier, so the
  member can pick again for that tier. If the picked golfer has already teed
  off, keep the original pick valid and scoring instead.
- Do not update tiers for a golfer who enters after the tournament's first tee
  shot; the entrant is not available to pick.
- Keep required league alerts in an in-app notification inbox for every
  affected member, and send device push notifications when enabled.
- Open edge case: how to handle a pre-tournament entrant for whom no usable
  betting odds are available.
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
- On Monday, projected values are replaced by official earnings and standings
  become final; a later source correction reopens and updates the affected
  results.
- Calculate projected live earnings from leaderboard positions and the purse;
  show the most up-to-date available figures. For tied leaderboard positions,
  split the projected payouts across all occupied places. Live calculations
  are visibly labeled as projected until official earnings are received.

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
- Resolve how to handle a pre-tournament entrant without usable odds.
- Decide the detailed late-pass rules if the pass is added later.
- Determine how admins manage counted tournaments and quarter boundaries
  in the admin interface.
- Resolve the data-model gaps: persisted tier snapshots, league tournament
  selection, quarter and score breakdowns, pick lock and swap history, tier
  validation, and late-pass tracking if included. Review earnings and year
  types for their expected ranges and API compatibility.
- Existing models contain per-golfer leaderboard tee times, but their presence
  does not establish that the API reliably supplies them.
