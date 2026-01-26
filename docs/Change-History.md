# Change History

**Last Updated:** 2026-01-26 15:18:18 UTC

**Period:** Last 11 commits

## Summary

| Metric | Count |
|--------|-------|
| **Total Commits** | 11 |
| **Active Contributors** | 2 |
| Structure Changes | 7 |
| Other Changes | 3 |
| Relationship Changes | 1 |

## Contributors

- **Ken**: 8 commit(s)
- **Mivangod**: 3 commit(s)

## Recent Changes


### 2026-01-26 (3 commits)

#### 📦 feat: reorganize pharyngeal structures into muscle and skeletal groups

*By Ken at 15:17 · [`584c24c`](../../commit/584c24cf4c9ca40a97427bff2c15fea83cfa2582)*

- ✏️ Modified 3 file(s)

**Files changed:**
- `structures/body_regions.yaml`
- `structures/muscles.yaml`
- `structures/skeletal.yaml`

#### 📦 feat: reorganize laryngeal structures and add reorganization parser

*By Ken at 15:10 · [`ab14e9f`](../../commit/ab14e9f239370057398af2c450ece9d6511d2b2a)*

- ✏️ Modified 3 file(s)

**Files changed:**
- `structures/body_regions.yaml`
- `structures/muscles.yaml`
- `structures/skeletal.yaml`

#### 📝 feat: reorganize tongue muscles into extrinsic and intrinsic subgroups

*By Ken at 15:02 · [`2794510`](../../commit/2794510173b4f049338d9f36cb76191f18ec6e5a)*

- ✏️ Modified 2 file(s)

**Files changed:**
- `structures/body_regions.yaml`
- `structures/muscles.yaml`


### 2026-01-21 (3 commits)

#### 📦 ADD hierarchy: Body (ID:12000) -> parent: (NULL - root node) (ID:None)     + ADD hierarchy: Eye Muscles (ID:12008) -> parent: Cranial muscles (ID:12007)     + ADD hierarchy: Inner Ear Muscles (ID:12009) -> parent: Cranial muscles (ID:12007)     + ADD hierarchy: External Ear Muscles (ID:12010) -> parent: Cranial muscles (ID:12007)     + ADD hierarchy: Ear Cavities (ID:20603) -> parent: Cavities and passages (ID:20006)     ~ UPDATE hierarchy: Stapedius (ID:26) -> parent: Inner Ear Muscles (ID:12009) [was: 9]     ~ UPDATE hierarchy: Tensor tympani (ID:22) -> parent: Inner Ear Muscles (ID:12009) [was: 9]     ~ UPDATE hierarchy: levator palpebrae superioris (ID:85) -> parent: Eye Muscles (ID:12008) [was: 8]     ~ UPDATE hierarchy: superior oblique muscle (ID:86) -> parent: Eye Muscles (ID:12008) [was: 8]     ~ UPDATE hierarchy: inferior oblique (ID:89) -> parent: Eye Muscles (ID:12008) [was: 8]     ~ UPDATE hierarchy: lateral rectus (ID:90) -> parent: Eye Muscles (ID:12008) [was: 8]     ~ UPDATE hierarchy: medial rectus (ID:91) -> parent: Eye Muscles (ID:12008) [was: 8]     ~ UPDATE hierarchy: superior rectus (ID:92) -> parent: Eye Muscles (ID:12008) [was: 8]     ~ UPDATE hierarchy: retractor bulbi (ID:93) -> parent: Eye Muscles (ID:12008) [was: 8]     ~ UPDATE hierarchy: Auricularis posterior (ID:98) -> parent: External Ear Muscles (ID:12010) [was: 9]     ~ UPDATE hierarchy: Auricularis anterior (ID:99) -> parent: External Ear Muscles (ID:12010) [was: 9]     ~ UPDATE hierarchy: Auricularis superior (ID:100) -> parent: External Ear Muscles (ID:12010) [was: 9]     ~ UPDATE hierarchy: nasal (ID:123) -> parent: Viscerocranium (ID:139) [was: 10]     ~ UPDATE hierarchy: vomer (ID:137) -> parent: Viscerocranium (ID:139) [was: 10]     ~ UPDATE hierarchy: external acoustic meatus (ID:96) -> parent: Ear Cavities (ID:20603) [was: 20702]     ~ UPDATE hierarchy: internal acoustic meatus (ID:97) -> parent: Ear Cavities (ID:20603) [was: 20301]

*By Ken at 17:20 · [`aa99809`](../../commit/aa998096c55041174d7cfdf46d5437df899ff495)*

- ✏️ Modified 3 file(s)

**Files changed:**
- `structures/body_regions.yaml`
- `structures/muscles.yaml`
- `structures/skeletal.yaml`

#### 📝 Helper script

*By Ken at 17:09 · [`55cdb12`](../../commit/55cdb12ed20e1f00e0616c594237360049477cba)*

- ✏️ Modified 1 file(s)

**Files changed:**
- `structures/body_regions.yaml`

#### 📝 feat: AI-generated changes from issue #11

*By Mivangod at 16:17 · [`e654e24`](../../commit/e654e2484ef9bd9aba4ce8568034bd8e622eb390)*

- ✏️ Modified 2 file(s)

**Files changed:**
- `relationships/developmental.yaml`
- `structures/body_regions.yaml`


### 2026-01-08 (5 commits)

#### 📦 fix: actually remove Tensor tympani structure and update README

*By Ken at 19:02 · [`5c6166f`](../../commit/5c6166fe20b48b73b4df37b4d9170ffe7f377e08)*

- ✏️ Modified 1 file(s)

**Files changed:**
- `structures/body_regions.yaml`

#### 🔗 fix: remove orphaned relationship after Tensor tympani deletion

*By Ken at 19:00 · [`fe58b43`](../../commit/fe58b4381b45782bead19a19ca78c6a11026cf17)*

- ✏️ Modified 1 file(s)

**Files changed:**
- `relationships/innervation.yaml`

#### 📦 fix: remove/deprecate structure from issue #3

*By Mivangod at 18:56 · [`d0a5768`](../../commit/d0a57689ca1d043ef88c6c08de5bfe00f2180a50)*

- ✏️ Modified 1 file(s)

**Files changed:**
- `structures/muscles.yaml`

#### 📦 feat: add structure from issue #1

*By Mivangod at 18:47 · [`c753f63`](../../commit/c753f63059198d0baf218838961b650d2e15ae55)*

- ✏️ Modified 1 file(s)

**Files changed:**
- `structures/body_regions.yaml`

#### 📦 Initial BAP ontology structure with Head and Neck hierarchies

*By Ken at 18:14 · [`f1fb7e6`](../../commit/f1fb7e6862ea44aef848ab4167a89d6a87065856)*



---
*Auto-generated change history*
