# BAP Marmoset Head Ontology

A collaborative repository for managing the Brain Architecture Project (BAP) 
Marmoset (Callithrix jacchus) head anatomical ontology.

## 📚 [**View the Auto-Generated Wiki →**](https://mitralab-organization.github.io/bap-ontology-editor/)

Complete documentation with detailed reports, statistics, and visualizations - 
**automatically updated on every push!**

## Overview

This repository provides a human-readable way to manage:
- **Anatomical structures** (muscles, nerves, blood vessels, bones)
- **Hierarchies** (parent-child relationships)
- **Biological relationships** (innervation, blood supply, developmental origins)

Changes are validated automatically via GitHub Actions and generate OWL files 
for use in WebProtégé and other tools.

## Species Information

- **Common name:** Marmoset
- **Scientific name:** Callithrix jacchus
- **NCBI Taxonomy:** 9483
- **Focus:** Head and neck anatomy

<!-- STATS_START -->
📊 **Ontology Statistics**
```
├── Structures: 805
├── Hierarchy depth: 11 levels
└── Relationships: 0
```
<!-- STATS_END -->

## Hierarchy

<!-- HIERARCHY_START -->
```
Body
├── Head
│   └── Brain
│       └── WHOLE BRAIN
│           ├── BRAIN STEM (MIDBRAIN+PONS+MEDULLA OBLONGATA)
│           │   ├── MEDULLA OBLONGATA (MYELENCEPHALON)
│           │   │   ├── Accessory nerve nucleus
│           │   │   ├── Ad1 adrenalin cells
│           │   │   ├── Ambiguus nucleus
│           │   │   │   ├── Ambiguus nucleus; compact part
│           │   │   │   └── Ambiguus nucleus; loose part
│           │   │   ├── Botzinger complex
│           │   │   ├── Conterminal nucleus
│           │   │   ├── Cuneate nucleus
│           │   │   ├── Dorsal motor nucleus of vagus; caudal part
│           │   │   ├── Epifacicular nucleus
│           │   │   ├── External cuneate nucleus
│           │   │   ├── Gracile nucleus
│           │   │   ├── Hypoglossal nucleus
│           │   │   ├── Hypoglossal nucleus; geniohyyoid part
│           │   │   ├── Inferior olive
│           │   │   │   ├── Inferior olive; beta subnucleus of the medial nucleus
│           │   │   │   ├── Inferior olive; cap of Kooy of the medial nucleus
│           │   │   │   ├── Inferior olive; dorsal nucleus
│           │   │   │   ├── Inferior olive; medial nucleus
│           │   │   │   ├── Inferior olive; principal nucleus
│           │   │   │   ├── Inferior olive; subnucleus A of medial nucleus
│           │   │   │   ├── Inferior olive; subnucleus B of medial nucleus
│           │   │   │   └── Inferior olive; subnucleus C of medial nucleus
│           │   │   ├── Inferior salivatory nucleus
│           │   │   ├── Intercalated nucleus
│           │   │   ├── Interstitial nucleus of the vestibular part of the 8th nerve
│           │   │   ├── Kolliker-Fuse nucleus
│           │   │   ├── Lateral pericuneate nucleus
│           │   │   ├── Lateral terminal nucleus of the accessory optic tract
│           │   │   ├── Linear nucleus of the hindbrain
│           │   │   ├── Matrix region of the medulla
│           │   │   ├── Median accessory nucleus of the medulla
│           │   │   ├── NA1 noradrenalin cells
│           │   │   ├── NA2 noradrenalin cells
│           │   │   ├── Noto cuneate nucleus
│           │   │   ├── Nucleus X
│           │   │   ├── Nucleus of Roller
│           │   │   ├── Nucleus of the spinal trigeminal tract
│           │   │   │   ├── Spinal trigeminal nucleus; caudal part
│           │   │   │   ├── Spinal trigeminal nucleus; interpolar part
│           │   │   │   └── Spinal trigeminal nucleus; oral part
│           │   │   ├── Parasolitary nucleus
│           │   │   ├── Paratrigeminal nucleus
│           │   │   ├── Prepositus nucleus
│           │   │   │   └── Prepositus nucleus; magnocellular part
│           │   │   ├── Raphe nuclei
│           │   │   │   ├── Raphe obscurus nucleus
│           │   │   │   └── Raphe pallidus nucleus
│           │   │   ├── Reticular formation
│           │   │   │   ├── Caudoventrolateral reticular nucleus
│           │   │   │   ├── Dorsal paragigantocellular nucleus
│           │   │   │   ├── Gigantocellular reticular nucleus
│           │   │   │   │   ├── Gigantocellular reticular nucleus; alpha part
│           │   │   │   │   └── Gigantocellular reticular nucleus; ventral part
│           │   │   │   ├── Intermediate reticular nucleus
│           │   │   │   ├── Lateral paragigantocellular nucleus
│           │   │   │   ├── Lateral reticular nucleus
│           │   │   │   │   ├── Lateral reticular nucleus; parvicellular part
│           │   │   │   │   └── Lateral reticular nucleus; subtrigeminal part
│           │   │   │   ├── Medullary reticular nucleus; dorsal part
│           │   │   │   ├── Medullary reticular nucleus; ventral part
│           │   │   │   ├── Parvicellular reticular nucleus
│           │   │   │   ├── Parvicellular reticular nucleus; alpha part
│           │   │   │   └── Rostroventrolateral reticular nucleus
│           │   │   ├── Retroambiguus nucleus
│           │   │   ├── Rostral ventral respiratory group
│           │   │   ├── Solitary nucleus
│           │   │   │   ├── Solitary nucleus; commissural part
│           │   │   │   ├── Solitary nucleus; dorsolateral part
│           │   │   │   ├── Solitary nucleus; gelatinous part
│           │   │   │   ├── Solitary nucleus; intermediate part
│           │   │   │   ├── Solitary nucleus; interstitial part
│           │   │   │   ├── Solitary nucleus; medial part
│           │   │   │   ├── Solitary nucleus; paracommissural part
│           │   │   │   ├── Solitary nucleus; rostrolateral part
│           │   │   │   ├── Solitary nucleus; ventral part
│           │   │   │   └── Solitary nucleus; ventrolateral part
│           │   │   ├── Superior salivatory nucleus
│           │   │   ├── Vagus nerve nucleus
│           │   │   └── Vestibular nuclei
│           │   │       ├── Lateral vestibular nucleus
│           │   │       ├── Medial vestibular nucleus
│           │   │       │   ├── Medial vestibular nucleus; magnocellular part
│           │   │       │   └── Medial vestibular nucleus; parvicellular part
│           │   │       ├── Nucleus Y of the vestibular complex
│           │   │       ├── Spinal vestibular nucleus
│           │   │       └── Superior vestibular nucleus
│           │   ├── MIDBRAIN (MESENCEPHALON)
│           │   │   ├── Commissural nucleus of the inferior colliculus
│           │   │   ├── DA8 dopamine cells
│           │   │   ├── Edinger-Westphal nucleus
│           │   │   ├── Inferior colliculus
│           │   │   │   ├── Central nucleus of the inferior colliculus
│           │   │   │   ├── Dorsal cortex of the inferior colliculus
│           │   │   │   └── External cortex of the inferior colliculus
│           │   │   ├── Interoculomotor nucleus
│           │   │   ├── Interpeduncular nucleus
│           │   │   │   ├── Interpeduncular nucleus; apical subnucleus
│           │   │   │   ├── Interpeduncular nucleus; caudal subnucleus
│           │   │   │   ├── Interpeduncular nucleus; intermediate subnucleus
│           │   │   │   ├── Interpeduncular nucleus; lateral subnucleus
│           │   │   │   └── Interpeduncular nucleus; rostral subnucleus
│           │   │   ├── Interstitial nucleus of Cajal
│           │   │   ├── Medial accessory oculomotor nucleus
│           │   │   ├── Mesencephalic trigeminal nucleus
│           │   │   ├── Nucleus of Darkschewitsch
│           │   │   ├── Nucleus of the brachium of the inferior colliculus
│           │   │   ├── Nucleus of the posterior commissure
│           │   │   ├── Occulomotor nucleus
│           │   │   ├── Occulomotor nucleus; parvicellular part
│           │   │   ├── Parabrachial pigmented nucleus of the VTA
│           │   │   ├── Parainterfascicular nucleus of the ventral tegmental area
│           │   │   ├── Paranigral nucleus of the VTA
│           │   │   ├── Periaqueductal gray
│           │   │   │   ├── Dorsolateral periaqueductal gray
│           │   │   │   ├── Dorsomedial periaqueductal gray
│           │   │   │   ├── Lateral periaqueductal gray
│           │   │   │   ├── Pleioglia periaqueductal gray
│           │   │   │   ├── Supraoculomotor cap
│           │   │   │   ├── Supraoculomotor periaqueductal gray
│           │   │   │   └── Ventrolateral periaqueductal gray
│           │   │   ├── Peripeduncular nucleus
│           │   │   ├── Prerubral field
│           │   │   ├── Raphe nuclei
│           │   │   │   ├── Dorsal raphe nucleus
│           │   │   │   │   ├── Dorsal raphe nucleus; caudal part
│           │   │   │   │   ├── Dorsal raphe nucleus; dorsal part
│           │   │   │   │   ├── Dorsal raphe nucleus; interfascicular part
│           │   │   │   │   ├── Dorsal raphe nucleus; lateral part
│           │   │   │   │   ├── Dorsal raphe nucleus; ventral part
│           │   │   │   │   └── Dorsal raphe nucleus; ventrolateral part
│           │   │   │   └── Rostral linear nucleus
│           │   │   ├── Red nucleus
│           │   │   │   ├── Red nucleus; magnocellular part
│           │   │   │   └── Red nucleus; parvicellular part
│           │   │   ├── Reticular formation
│           │   │   │   ├── Cuneinform nucleus
│           │   │   │   ├── Mesencephlic reticular formation
│           │   │   │   └── Precuneiform area
│           │   │   ├── Rostral interstitial nucleus of the medial longitudinal fasciculus
│           │   │   ├── Subbrachial nucleus
│           │   │   ├── Substantia nigra
│           │   │   ├── Superior colliculus
│           │   │   │   ├── Deep gray layer of the superior colliculus
│           │   │   │   ├── Deep white layer of the superior colliculus
│           │   │   │   ├── Intermediate gray layer of the superior colliculus
│           │   │   │   ├── Intermediate white layer of the superior colliculus
│           │   │   │   ├── Optic nerve layer of the superior colliculus
│           │   │   │   ├── Superficial gray layer of the superior colliculcus
│           │   │   │   └── Zonal layer of the superior colliculus
│           │   │   ├── Trochlear nucleus
│           │   │   └── Ventral tegmental area
│           │   │       ├── Ventral tegmental area; caudal part
│           │   │       └── Ventral tegmental area; rostral part
│           │   └── PONS (METENCEPHALON)
│           │       ├── Abducens nucleus
│           │       ├── Anterior tegmental nucleus
│           │       ├── B9 serotonin cells
│           │       ├── Barrington's nucleus
│           │       ├── Central gray
│           │       ├── Cochlear nuclei
│           │       │   ├── Dorsal cochlear nucleus
│           │       │   ├── Granule cell layer of the cochlear nuclei
│           │       │   ├── Ventral cochlear nucleus; anterior part
│           │       │   └── Ventral cochlear nucleus; posterior part
│           │       ├── Dorsal nucleus of the lateral lemniscus
│           │       ├── Dorsal tegmental nucleus
│           │       ├── Facial motor nucleus; stylohyoid part
│           │       ├── Facial nucleus
│           │       ├── Intermediate nucleus of the lateral lemniscus
│           │       ├── Laterodorsal tegmental nucleus
│           │       ├── Laterodorsal tegmental nucleus; ventral part
│           │       ├── Locus coeruleus
│           │       ├── Medial paralemniscial nucleus
│           │       ├── Microcellular tegmental nucleus
│           │       ├── Motor trigeminal nucleus
│           │       ├── Motor trigeminal nucleus; parvicellular part
│           │       ├── NA5 noradrenalin cells
│           │       ├── NA7 noradrenalin cells
│           │       ├── Nucleus of the central acoustic tract
│           │       ├── Nucleus of the spinal trigeminal tract
│           │       ├── Nucleus of the trapezoid body
│           │       ├── Parabigeminal nucleus
│           │       ├── Parabrachial nuclei
│           │       │   ├── Lateral parabrachial nucleus
│           │       │   │   ├── Lateral parabrachial nucleus; central part
│           │       │   │   ├── Lateral parabrachial nucleus; crescent part
│           │       │   │   ├── Lateral parabrachial nucleus; dorsal part
│           │       │   │   ├── Lateral parabrachial nucleus; external part
│           │       │   │   ├── Lateral parabrachial nucleus; internal part
│           │       │   │   ├── Lateral parabrachial nucleus; superior part
│           │       │   │   └── Lateral parabrachial nucleus; ventral part
│           │       │   ├── Medial parabrachial nucleus
│           │       │   └── Medial parabrachial nucleus external part
│           │       ├── Paralemniscal nucleus
│           │       ├── Pedunculotegmental nucleus
│           │       ├── Peritrigeminal zone
│           │       ├── Pontine nuclei
│           │       ├── Posterodorsal tegmental nucleus
│           │       ├── Principal sensory trigeminal nucleus
│           │       │   ├── Principal sensory trigeminal nucleus; dorsomedial part
│           │       │   └── Principal sensory trigeminal nucleus; ventrolateral part
│           │       ├── Raphe nuclei
│           │       │   ├── Caudal linear nucleus of the raphe
│           │       │   ├── Dorsal raphe nucleus; caudal part
│           │       │   ├── Median raphe nucleus
│           │       │   ├── Paramedian raphe nucleus
│           │       │   ├── Raphe interpositus nucleus
│           │       │   └── Raphe magnus nucleus
│           │       ├── Reticular formation
│           │       │   ├── Pontine reticular nucleus; caudal part
│           │       │   ├── Pontine reticular nucleus; oral part
│           │       │   ├── Pontine reticular nucleus; ventral part
│           │       │   ├── Reticulotegmental nucleus of the pons
│           │       │   └── Reticulotegmental nucleus of the pons; lateral part
│           │       ├── Retroisthmic nucleus
│           │       ├── Retrolemniscal nucleus
│           │       ├── Rhabdoid nucleus
│           │       ├── Sagulum nucleus
│           │       ├── Subcoeruleus nucleus; dorsal part
│           │       ├── Subcoeruleus nucleus; ventral part
│           │       ├── Subpeduncular tegmental nucleus
│           │       ├── Superior olive
│           │       │   ├── Dorsal periolivary region
│           │       │   ├── Lateral superior olive
│           │       │   ├── Lateroventral periolivary nucleus
│           │       │   ├── Medial superior olive
│           │       │   ├── Medioventral periolivary nucleus
│           │       │   └── Superior paraolivary nucleus
│           │       ├── Supratrigeminal nucleus
│           │       ├── Triangular nucleus of the lateral lemniscus
│           │       ├── Ventral nucleus of the lateral lemniscus
│           │       └── Vestibular nuclei
│           ├── CEREBELLUM (METENCEPHALON)
│           │   ├── Cerebellar cortex
│           │   │   ├── Copula of the pyramis
│           │   │   ├── Crus1 of the ansiform lobule
│           │   │   ├── Crus2 of the ansiform lobule
│           │   │   ├── Flocculus
│           │   │   ├── Lobule 1 of cerebellar vermis (lingula)
│           │   │   ├── Lobule 10 of cerebellar vermis (nodule)
│           │   │   ├── Lobule 2 of cerebellar vermis
│           │   │   ├── Lobule 3 of cerebellar vermis
│           │   │   ├── Lobule 4 of cerebellar vermis
│           │   │   ├── Lobule 5 of cerebellar vermis
│           │   │   ├── Lobule 6 of cerebellar vermis
│           │   │   ├── Lobule 7 of cerebellar vermis
│           │   │   ├── Lobule 8 of cerebellar vermis
│           │   │   ├── Lobule 9 of cerebellar vermis (uvula)
│           │   │   ├── Paraflocculus
│           │   │   ├── Paramedian lobule
│           │   │   └── Simple lobule
│           │   ├── Deep cerebellar nuclei
│           │   │   ├── Anterior interposed cerebellar nucleus
│           │   │   ├── Lateral (dentate) cerebellar nucleus
│           │   │   ├── Lateral cerebellar nucleus; parvicellular part
│           │   │   ├── Medial cerebellar nucleus
│           │   │   ├── Posterior interposed cerebellar nucleus
│           │   │   └── Vestibulocerebellar nucleus
│           │   └── Superior medullary velum
│           ├── CIRCUMVENTRICULAR ORGAN
│           │   ├── Area postrema
│           │   ├── Median eminence
│           │   ├── Neurohypophysis
│           │   ├── Pineal gland
│           │   ├── Subcommissural organ
│           │   ├── Subfornical organ
│           │   └── Vascular organ of the lamina terminalis
│           ├── CRANIAL NERVE
│           │   ├── Abducens nerve
│           │   ├── Cochlear root of the vestibulocochlear nerve
│           │   ├── Facial nerve
│           │   ├── Hypoglossal nerve
│           │   ├── Nervus intermedius component of facial nerve
│           │   ├── Occulomotor nerve
│           │   ├── Optic nerve
│           │   ├── Trigeminal nerve
│           │   ├── Trochlear nerve
│           │   ├── Vestibular root of the vestibulocochlear nerve
│           │   └── Vestibulocochlear nerve
│           ├── FIBER BUNDLE
│           │   ├── Alveus of the hippocampus
│           │   ├── Ansa lenticularis
│           │   ├── Anterior commissure
│           │   ├── Anterior commissure; anterior part
│           │   ├── Anterior commissure; intrabulbar part
│           │   ├── Anterior commissure; posterior limb
│           │   ├── Ascending fibers of the facial nerve
│           │   ├── Brachium of the inferior colliculus
│           │   ├── Brachium of the superior colliculus
│           │   ├── Cerebral peduncle
│           │   ├── Cingulum
│           │   ├── Commissural stria terminals
│           │   ├── Commissure of the inferior colliculus
│           │   ├── Commissure of the lateral leminiscus
│           │   ├── Commissure of the superior colliculus
│           │   ├── Corpus callosum
│           │   ├── Cuneate fascicolus
│           │   ├── Decussation of the medial lemniscus
│           │   ├── Decussation of the superior cerebellar peduncle
│           │   ├── Dorsal spinocerebellar tract
│           │   ├── Dorsal tegmental decussation
│           │   ├── Dosal acoustic atria
│           │   ├── Dosal corticospinal tract
│           │   ├── External capsule
│           │   ├── External medullary lamina
│           │   ├── Extreme capsule
│           │   ├── Fasciculus retroflexus
│           │   ├── Finbria of the hippocampus
│           │   ├── Forceps minor corpus callosum
│           │   ├── Fornix
│           │   ├── Genu of the corpus callosum
│           │   ├── Genu of the facial nerve
│           │   ├── Gracile fasciculus
│           │   ├── Habenular commissure
│           │   ├── Inferior cerebellar peduncle
│           │   ├── Internal capsule
│           │   ├── Lateral corticospinal tract
│           │   ├── Lateral lemniscus
│           │   ├── Lateral medullary lamina
│           │   ├── Lateral olfactory tract
│           │   ├── Longitudinal fasciculs of the pons
│           │   ├── Mammillary peduncle
│           │   ├── Mammillotegmental tract
│           │   ├── Mammillothalamic tract
│           │   ├── Medial forebrain bundle
│           │   ├── Medial lemniscus
│           │   ├── Medial longitudinal faciculcus
│           │   ├── Medial medullar lamina
│           │   ├── Mesencephalic trigeminal tract
│           │   ├── Middle cerebellar peduncle
│           │   ├── Motor root of the trigeminal nerve
│           │   ├── Nigrostriatal bundle
│           │   ├── Olivocerebellar tract
│           │   ├── Olivocochlear bundle
│           │   ├── Optic chiasm
│           │   ├── Optic tract
│           │   ├── Palidohypothalamic tract
│           │   ├── Posterior commissure
│           │   ├── Pyramidal decussation
│           │   ├── Pyramidal tract
│           │   ├── Retromammillary decussation
│           │   ├── Rostrum of the corpus callosum
│           │   ├── Rubrospinal tract
│           │   ├── Sensory root of the trigeminal nerve
│           │   ├── Solitary tract
│           │   ├── Spinal trigeminal tract
│           │   ├── Stria medullaris of the thalamus
│           │   ├── Stria terminalis
│           │   ├── Superior cerebellar peduncle
│           │   ├── Supraoptic decussation
│           │   ├── Tectospinal tract
│           │   ├── Transverse fibers of the pons
│           │   ├── Trapezoid body
│           │   ├── Ventral hippocampal commissure
│           │   ├── Ventral spinocerebellar tract
│           │   ├── Ventral tegmental decussation
│           │   ├── Vestibulomesencephalic tract
│           │   ├── h1 fasciculus (thalamic fasciculus)
│           │   └── h2 fasciculus (lenticular fasciculus)
│           ├── FOREBRAIN (TELENCEPHALON and DIENCEPHALON)
│           │   ├── DIENCEPHALON
│           │   │   ├── EPITHALAMUS
│           │   │   │   ├── Habenular nucleus
│           │   │   │   │   ├── Lateral habenular nucleus
│           │   │   │   │   └── Medial habenular nucleus
│           │   │   │   └── Paraventricular thalamic nucleus
│           │   │   │       ├── Paraventricular thalamic nucleus; anterior part
│           │   │   │       └── Paraventricular thalamic nucleus; posterior part
│           │   │   ├── HYPOTHALAMUS
│           │   │   │   ├── Anterior hypothalamic area; anterior part
│           │   │   │   ├── Anterior hypothalamic nucleus
│           │   │   │   ├── Anteroventral periventricular nucleus
│           │   │   │   ├── Arcuate hypothalamic nucleus
│           │   │   │   ├── DA11 dopamine cells
│           │   │   │   ├── DA12 dopamine cells
│           │   │   │   ├── DA14 dopamine cells
│           │   │   │   ├── Dorsomedial hypothalamic nucleus
│           │   │   │   ├── Dorsomedial hypothalamic nucleus; compact part
│           │   │   │   ├── Juxtaparaventricular part of the lateral hypothalamus
│           │   │   │   ├── Lamina terminalis
│           │   │   │   ├── Lateral hypothalamic area
│           │   │   │   ├── Mammillary body
│           │   │   │   │   ├── Lateral mammillary nucleus
│           │   │   │   │   ├── Medial mammillary nucleus; lateral part
│           │   │   │   │   └── Medial mammillary nucleus; medial part
│           │   │   │   ├── Medial tuberal nucleus
│           │   │   │   ├── Nucleus of the stria medullaris
│           │   │   │   ├── Paraventricular hypothalamic nucleus
│           │   │   │   │   ├── Paraventricular hypothalamic nucleus; dorsal cap
│           │   │   │   │   ├── Paraventricular hypothalamic nucleus; lateral magnocellular part
│           │   │   │   │   └── Paraventricular hypothalamic nucleus; posterior part
│           │   │   │   ├── Perifornical nucleus
│           │   │   │   ├── Periventricular hypothalamic nucleus
│           │   │   │   ├── Posterior hypothalamic nucleus
│           │   │   │   ├── Premammillary nucleus; dorsal part
│           │   │   │   ├── Premammillary nucleus; ventral part
│           │   │   │   ├── Preoptic area
│           │   │   │   │   ├── Lateral preoptic area
│           │   │   │   │   ├── Medial preoptic area
│           │   │   │   │   ├── Medial preoptic nucleus
│           │   │   │   │   └── Median preoptic nucleus
│           │   │   │   ├── Retromammillary nucleus
│           │   │   │   ├── Striohypothalamic nucleus
│           │   │   │   ├── Suprachiasmatic nucleus
│           │   │   │   ├── Supraoptic nucleus
│           │   │   │   ├── Supraoptic nucleus; retrochiasmatic part
│           │   │   │   ├── Ventral tuberomammillary nucleus
│           │   │   │   ├── Ventrolateral preoptic nucleus
│           │   │   │   ├── Ventromedial hypothalamic nucleus
│           │   │   │   └── Ventromedial preoptic nucleus
│           │   │   ├── PRETECTUM
│           │   │   │   ├── Anterior pretectal nucleus
│           │   │   │   ├── Magnocellular nucleus of the posterior commissure
│           │   │   │   ├── Medial pretectal area
│           │   │   │   ├── Nucleus of the optic tract
│           │   │   │   ├── Olivary pretectal nucleus
│           │   │   │   ├── Precommissural nucleus
│           │   │   │   └── Retrocommissural nucleus
│           │   │   └── THALAMUS
│           │   │       ├── Association nuclei
│           │   │       │   ├── Anterior nuclei
│           │   │       │   │   ├── Anterodorsal thalamic nucleus
│           │   │       │   │   ├── Anteromedial thalamic nucleus
│           │   │       │   │   └── Anteroventral thalamic nucleus
│           │   │       │   ├── Lateral nuclei
│           │   │       │   │   ├── Lateral posterior thalamic nucleus
│           │   │       │   │   └── Laterodorsal thalamic nucleus
│           │   │       │   ├── Mediodorsal thalamic nucleus
│           │   │       │   │   ├── Mediodorsal thalamic nucleus; central part
│           │   │       │   │   ├── Mediodorsal thalamic nucleus; lateral part
│           │   │       │   │   └── Mediodorsal thalamic nucleus; medial part
│           │   │       │   ├── Paratenial nucleus
│           │   │       │   └── Pulvinar
│           │   │       │       ├── Anterior pulvinar
│           │   │       │       ├── Inferior pulvinar
│           │   │       │       ├── Inferior pulvinar; caudolateral part
│           │   │       │       ├── Inferior pulvinar; caudomedial part
│           │   │       │       ├── Inferior pulvinar; medial part
│           │   │       │       ├── Inferior pulvinar; posterior part
│           │   │       │       ├── Lateral pulvinar
│           │   │       │       └── Medial pulvinar
│           │   │       ├── Auditory thalamus
│           │   │       │   └── Medial geniculate nucleus
│           │   │       │       ├── Medial geniculate nucleus; dorsal part
│           │   │       │       ├── Medial geniculate nucleus; medial part
│           │   │       │       └── Medial geniculate nucleus; ventral part
│           │   │       ├── Midline and intralaminar nuclei
│           │   │       │   ├── Angular thalamic nucleus
│           │   │       │   ├── Central medial thalamic nucleus
│           │   │       │   ├── Centrolateral thalamic nucleus
│           │   │       │   ├── Centromedian thalamic nucleus
│           │   │       │   ├── Interanteromedial thalamic nucleus
│           │   │       │   ├── Intermediodorsal thalamic nucleus
│           │   │       │   ├── Oval paracentral thalamic nucleus
│           │   │       │   ├── Paracentral thalamic nucleus
│           │   │       │   ├── Parafascicular thalamic nucleus
│           │   │       │   ├── Posterior intralaminar thalamic nucleus
│           │   │       │   ├── Posterior limitans thalamic nucleus
│           │   │       │   ├── Retroreuniens nucleus
│           │   │       │   ├── Reuniens thalamic nucleus
│           │   │       │   ├── Rhomboid thalamic nucleus
│           │   │       │   └── Xiphoid thalamic nucleus
│           │   │       ├── Motor thalamus
│           │   │       │   ├── Ventral anterior thalamic nucleus
│           │   │       │   │   ├── Ventral anterior thalamic nucleus; lateral part
│           │   │       │   │   ├── Ventral anterior thalamic nucleus; magnocellular part
│           │   │       │   │   └── Ventral anterior thalamic nucleus; medial part
│           │   │       │   └── Ventral lateral thalamic nucleus
│           │   │       │       ├── Ventral lateral thalamic nucleus; lateral part
│           │   │       │       ├── Ventral lateral thalamic nucleus; medial part
│           │   │       │       ├── Ventrolateral thalamic nucleus; dorsal part
│           │   │       │       └── Ventrolateral thalamic nucleus; ventral part
│           │   │       ├── Somatosensory thalamus
│           │   │       │   ├── Ethmoid thalamic nucleus
│           │   │       │   ├── Posterior thalamic nuclear group
│           │   │       │   ├── Posterior thalamic nuclear group; triangular part
│           │   │       │   ├── Suprageniculate thalamic nucleus
│           │   │       │   ├── Ventoposterior complex
│           │   │       │   │   ├── Ventral posterior nucleus of the thalamus; parvicellular
│           │   │       │   │   ├── Ventral posterolateral thalamic nucleus
│           │   │       │   │   └── Ventral posteromedial thalamic nucleus
│           │   │       │   ├── Ventral posterior thalamic nucleus; inferior part
│           │   │       │   └── Ventral posterior thalamic nucleus; superior part
│           │   │       ├── Ventral thalamus
│           │   │       │   ├── Parasubthalamic nucleus
│           │   │       │   ├── Reticular nucleus
│           │   │       │   ├── Subgeniculate nucleus of prethalamus
│           │   │       │   ├── Subincertal nucleus
│           │   │       │   ├── Subparafiscicular thalamic nucleus
│           │   │       │   ├── Subparafiscicular thalamic nucleus; parvicellular part
│           │   │       │   └── Zona incerta
│           │   │       │       ├── Zuna incerta; caudal part
│           │   │       │       ├── Zuna incerta; dorsal part
│           │   │       │       ├── Zuna incerta; rostral part
│           │   │       │       └── Zuna incerta; ventral part
│           │   │       └── Visual thalamus
│           │   │           └── Dorsal lateral geniculate nucleus
│           │   │               ├── External magnocellular layer of the dorsal lateral geniculate
│           │   │               ├── External parvicellular layer of the dorsal lateral geniculate
│           │   │               ├── Internal magnocellular layer of the dorsal lateral geniculate
│           │   │               ├── Internal parvicellular layer of the dorsal lateral geniculate
│           │   │               ├── Koniocellular layer of dorsal latral geniculate K1
│           │   │               ├── Koniocellular layer of dorsal latral geniculate K2
│           │   │               ├── Koniocellular layer of dorsal latral geniculate K3
│           │   │               ├── Koniocellular layer of dorsal latral geniculate K4
│           │   │               └── Pregeniculate nucleus
│           │   └── TELENCEPHALON
│           │       ├── BASAL GANGLIA
│           │       │   ├── Amygdala
│           │       │   │   ├── Amygdalohippocampal area
│           │       │   │   ├── Amygdalopiriform transition area
│           │       │   │   ├── Amygdalostriatal transition area
│           │       │   │   ├── Cortex-amygdala transition zone
│           │       │   │   ├── Cortical amygdaloid group (corticomedial group)
│           │       │   │   │   ├── Central amygdaloid nucleus
│           │       │   │   │   │   ├── Central amygdaloid nucleus; capsular parts
│           │       │   │   │   │   ├── Central amygdaloid nucleus; lateral parts
│           │       │   │   │   │   └── Central amygdaloid nucleus; medial parts
│           │       │   │   │   ├── Cortical amugdaloid nucleus
│           │       │   │   │   │   ├── Anterior amygdaloid area
│           │       │   │   │   │   ├── Anterior cortical amygdaloid nucleus
│           │       │   │   │   │   ├── Nucleus of the lateral olfactry tract
│           │       │   │   │   │   └── Posterior cortical amygdaloid nucleus
│           │       │   │   │   └── Medial amygdaloid nucleus
│           │       │   │   ├── Extended amygdala
│           │       │   │   │   ├── Extended amygdala
│           │       │   │   │   │   └── Bed nucleus of the stria terminalis
│           │       │   │   │   ├── Intercalated amygdaloid nucleus; main part
│           │       │   │   │   ├── Intercalated nuclei of the amygdala
│           │       │   │   │   └── Interstitial nucleus of the posterior limb of the anterior commissure
│           │       │   │   ├── Latero-basal nuclear complex (bassolateral group)
│           │       │   │   │   ├── Basolateral amygdaloid nucleus
│           │       │   │   │   │   ├── Basolateral amygdaloid nucleus; dorsal part
│           │       │   │   │   │   ├── Basolateral amygdaloid nucleus; dorsolateral part
│           │       │   │   │   │   ├── Basolateral amygdaloid nucleus; intermediate part
│           │       │   │   │   │   ├── Basolateral amygdaloid nucleus; ventrolateral part
│           │       │   │   │   │   └── Basolateral amygdaloid nucleus; ventromedial part
│           │       │   │   │   ├── Basomedial amygdaloid nucleus
│           │       │   │   │   │   ├── Basomedial amygdaloid nucleus; dorsal part
│           │       │   │   │   │   ├── Basomedial amygdaloid nucleus; magnocellular part
│           │       │   │   │   │   ├── Basomedial amygdaloid nucleus; parvicellular part
│           │       │   │   │   │   ├── Basomedial amygdaloid nucleus; vebtromedial part
│           │       │   │   │   │   └── Basomedial amygdaloid nucleus; ventral part
│           │       │   │   │   └── Lateral amygdaloid nucleus
│           │       │   │   └── Paralaminar amygdaloid nucleus
│           │       │   ├── Basal nucleus (Meynert)
│           │       │   ├── Claustrum
│           │       │   ├── Dorsal nucleus of the endopiriform claustrum
│           │       │   ├── Globus pallidus
│           │       │   │   ├── External globus pallidus
│           │       │   │   └── Internal globus pallidus
│           │       │   ├── Intermediate endopiriform nucleus
│           │       │   ├── Striatum
│           │       │   │   ├── Accumbens nucleus
│           │       │   │   │   ├── Accumbens nucleus; core
│           │       │   │   │   └── Accumbens nucleus;shell
│           │       │   │   │       ├── Dorsal accumbens shell
│           │       │   │   │       ├── Lateral accumbens shell
│           │       │   │   │       └── Medial accumbens shell
│           │       │   │   ├── Caudate nucleus
│           │       │   │   └── Putamen
│           │       │   ├── Substania innominata; basal part
│           │       │   ├── Substantia nigra
│           │       │   │   ├── Substantia nigra; compact part
│           │       │   │   │   ├── Substantia nigra; compact part; dorsal tier
│           │       │   │   │   ├── Substantia nigra; compact part; medial tier
│           │       │   │   │   └── Substantia nigra; compact part; ventral tier
│           │       │   │   ├── Substantia nigra; lateral part
│           │       │   │   └── Substantia nigra; reticular part
│           │       │   ├── Subthalamic nucleus
│           │       │   ├── Ventral nucleus of the endopiriform claustrum
│           │       │   └── Ventral pallidum
│           │       ├── CEREBRUM;CEREBRAL CORTEX
│           │       │   ├── Cortical areas
│           │       │   │   ├── Anterior Cingulate Cortex
│           │       │   │   │   ├── Area 24a of cortex
│           │       │   │   │   ├── Area 24b of cortex
│           │       │   │   │   ├── Area 24c of cortex
│           │       │   │   │   └── Area 24d of cortex
│           │       │   │   ├── Auditory Cortex
│           │       │   │   │   ├── Auditory cortex; anterolateral area
│           │       │   │   │   ├── Auditory cortex; caudal parabelt area
│           │       │   │   │   ├── Auditory cortex; caudolateral area
│           │       │   │   │   ├── Auditory cortex; caudomedial area
│           │       │   │   │   ├── Auditory cortex; middle lateral area
│           │       │   │   │   ├── Auditory cortex; primary area
│           │       │   │   │   ├── Auditory cortex; rostral area
│           │       │   │   │   ├── Auditory cortex; rostral parabelt
│           │       │   │   │   ├── Auditory cortex; rostromedial area
│           │       │   │   │   ├── Auditory cortex; rostrotemporal lateral area
│           │       │   │   │   ├── Auditory cortex; rostrotemporal medial area
│           │       │   │   │   ├── Auditory cortex; rostrotemporal part
│           │       │   │   │   ├── Superior temporal rostral area
│           │       │   │   │   └── Temporoparietal transitional area
│           │       │   │   ├── Dorsolateral Prefrontal Cortex
│           │       │   │   │   ├── Area 10 of cortex
│           │       │   │   │   ├── Area 46 of cortex; dorsal part
│           │       │   │   │   ├── Area 46 of cortex; ventral part
│           │       │   │   │   ├── Area 8a of cortex; dorsal part
│           │       │   │   │   ├── Area 8a of cortex; ventral part
│           │       │   │   │   ├── Area 8b of cortex
│           │       │   │   │   └── Area 9 of cortex
│           │       │   │   ├── Faciola cinereum
│           │       │   │   ├── Indusium griseum
│           │       │   │   ├── Insular Cortex
│           │       │   │   │   ├── Agranular insular cortex
│           │       │   │   │   ├── Dysgranular insular cortex
│           │       │   │   │   ├── Granular insular cortex
│           │       │   │   │   ├── Insular proisocortex
│           │       │   │   │   ├── Parainsular cortex; lateral part
│           │       │   │   │   ├── Parainsular cortex; medial part
│           │       │   │   │   ├── Retroinsular area
│           │       │   │   │   └── Temporal proisocortex
│           │       │   │   ├── Lateral and Inferior Temporal Cortical Region
│           │       │   │   │   ├── Parietal areas PGa and IPa (fundus of superior temporal ventral area)
│           │       │   │   │   ├── Temporal area TE1
│           │       │   │   │   ├── Temporal area TE2
│           │       │   │   │   ├── Temporal area TE3
│           │       │   │   │   ├── Temporal area TE; occipital part
│           │       │   │   │   ├── Temporo-parieto-occipital association area (superior temporal polysensory cortex)
│           │       │   │   │   └── Temporopolar proisocortex
│           │       │   │   ├── Medial Prefrontal Cortex
│           │       │   │   │   ├── Area 14 of cortex; caudal part
│           │       │   │   │   ├── Area 14 of cortex; rostral part
│           │       │   │   │   ├── Area 25 of cortex
│           │       │   │   │   ├── Area 32 of cortex
│           │       │   │   │   └── Area 32 of cortex; ventral part
│           │       │   │   ├── Motor and Premotor Cortical Regions
│           │       │   │   │   ├── Area 4 of cortex; part c (primary motor)
│           │       │   │   │   ├── Area 4 of cortex; parts a and b (primary motor)
│           │       │   │   │   ├── Area 6 of cortex; dorsocaudal part
│           │       │   │   │   ├── Area 6 of cortex; dorsorostral part
│           │       │   │   │   ├── Area 6 of cortex; medial (supplementary motor) part
│           │       │   │   │   ├── Area 6 of cortex; ventral; part a
│           │       │   │   │   ├── Area 6 of cortex; ventral; part b
│           │       │   │   │   └── Area 8 of cortex; caudal part
│           │       │   │   ├── Navicular nucleus of the basal forebrain
│           │       │   │   ├── Orbital Frontal Cortex
│           │       │   │   │   ├── Area 11 of cortex
│           │       │   │   │   ├── Area 13 of cortex; lateral part
│           │       │   │   │   ├── Area 13 of cortex; medial part
│           │       │   │   │   ├── Area 13a of cortex
│           │       │   │   │   ├── Area 13b of cortex
│           │       │   │   │   ├── Gustatory cortex
│           │       │   │   │   ├── Orbital periallocortex
│           │       │   │   │   └── Orbital proisocortex
│           │       │   │   ├── Parasubiculum
│           │       │   │   ├── Piriform cortex
│           │       │   │   ├── Piriform cortex; layer 1
│           │       │   │   ├── Piriform cortex; layer 2
│           │       │   │   ├── Piriform cortex; layer 3
│           │       │   │   ├── Posterior Cingulate Medial and Retrosplenial Cortical Regions
│           │       │   │   │   ├── Area 23 of cortex; ventral part
│           │       │   │   │   ├── Area 23a of cortex
│           │       │   │   │   ├── Area 23b of cortex
│           │       │   │   │   ├── Area 23c of cortex
│           │       │   │   │   ├── Area 29a-c of cortex
│           │       │   │   │   ├── Area 29d of cortex
│           │       │   │   │   ├── Area 30 of cortex
│           │       │   │   │   ├── Area 31 of cortex
│           │       │   │   │   ├── Parietal area PG; medial part
│           │       │   │   │   └── Prostriate area
│           │       │   │   ├── Posterior Parietal Cortex
│           │       │   │   │   ├── Anterior intraparietal area of cortex
│           │       │   │   │   ├── Lateral intrapartietal area of cortex
│           │       │   │   │   ├── Medial intraparietal area of cortex
│           │       │   │   │   ├── Occipito-parietal transitional area of cortex
│           │       │   │   │   ├── Parietal area PE
│           │       │   │   │   ├── Parietal area PE; caudal part
│           │       │   │   │   ├── Parietal area PF
│           │       │   │   │   ├── Parietal area PFG
│           │       │   │   │   ├── Parietal area PG
│           │       │   │   │   └── Ventral intraparietal area of cortex
│           │       │   │   ├── Presubiculum
│           │       │   │   ├── Prosubiculum
│           │       │   │   ├── Somatosensory Cortex
│           │       │   │   │   ├── Area 3a of cortex (primary somatosensory)
│           │       │   │   │   ├── Area 3b of cortex (primary somatosensory)
│           │       │   │   │   ├── Areas 1 and 2 of cortex
│           │       │   │   │   ├── Secondary somatosensory cortex; external part
│           │       │   │   │   ├── Secondary somatosensory cortex; internal part
│           │       │   │   │   ├── Secondary somatosensory cortex; parietal rostral area
│           │       │   │   │   └── Secondary somatosensory cortex; parietal ventral area
│           │       │   │   ├── Supracallosal subiculum
│           │       │   │   ├── Ventral Areas of the Temporal Lobe
│           │       │   │   │   ├── Area 35 of cortex
│           │       │   │   │   ├── Area 36 of cortex
│           │       │   │   │   ├── Entorhinal cortex
│           │       │   │   │   ├── Temporal area TF
│           │       │   │   │   ├── Temporal area TF; occipital part
│           │       │   │   │   ├── Temporal area TH
│           │       │   │   │   ├── Temporal area TL
│           │       │   │   │   └── Temporal area TL; occipital part
│           │       │   │   ├── Ventrolateral Prefrontal Cortex
│           │       │   │   │   ├── Area 45 of cortex
│           │       │   │   │   ├── Area 47 (old 12) of cortex; lateral part
│           │       │   │   │   ├── Area 47 (old 12) of cortex; medial part
│           │       │   │   │   ├── Area 47 (old 12) of cortex; orbital part
│           │       │   │   │   └── Proisocortical motor region (precentral opercular cortex)
│           │       │   │   └── Visual Cortex
│           │       │   │       ├── Area 19 of cortex; dorsointermediate part
│           │       │   │       ├── Area 19 of cortex; medial part
│           │       │   │       ├── Fundus of superior temporal sulcus area of cortex
│           │       │   │       ├── Medial superior temporal area of cortex
│           │       │   │       ├── Visual area 1
│           │       │   │       ├── Visual area 2
│           │       │   │       ├── Visual area 3 (ventrolateral posterior area)
│           │       │   │       ├── Visual area 3A (dorsoanterior area)
│           │       │   │       ├── Visual area 4 (ventrolatereral anterior area)
│           │       │   │       ├── Visual area 4; transitional part
│           │       │   │       ├── Visual area 5 (middle temporal area)
│           │       │   │       ├── Visual area 6 (dorsomedial area)
│           │       │   │       └── Visual area 6A (posterior parietal medial area)
│           │       │   ├── Hippocampal formation
│           │       │   │   ├── Dentate gyrus
│           │       │   │   │   ├── Granule cell layer of the dentate gyrus
│           │       │   │   │   ├── Molecular layer of the dentate gyrus
│           │       │   │   │   └── Polymorph layer of the dentate gyrus
│           │       │   │   ├── Hippocampus
│           │       │   │   │   ├── Field CA1 of the hippocampus
│           │       │   │   │   ├── Field CA2 of the hippocampus
│           │       │   │   │   ├── Field CA3 of the hippocampus
│           │       │   │   │   ├── Lacunosum moleculare layer of the hippocampus
│           │       │   │   │   ├── Oriens layer of the hippocampus
│           │       │   │   │   ├── Pyramidal cell layer of the hippocampus
│           │       │   │   │   ├── Radiatum layer of the hippocampus
│           │       │   │   │   └── Stratum lucidum of the hippocampus
│           │       │   │   └── Subiculum
│           │       │   └── Olfactory cortex
│           │       │       ├── Olfactry tubercle
│           │       │       │   ├── Islands of Calleja
│           │       │       │   └── Islands of Calleja; major island
│           │       │       └── Tenia tecta
│           │       ├── OLFACTORY BULB
│           │       │   └── Olfactory bulb
│           │       │       ├── Accessory olfactory bulb
│           │       │       ├── Anterior olfactory nucleus
│           │       │       ├── Ependyma & subependymal layer
│           │       │       ├── External plexiform layer of the accessory olfactory bulb
│           │       │       ├── External plexiform layer of the olfactory bulb
│           │       │       ├── Glomerular layer of the accessory olfactory bulb
│           │       │       ├── Glomerular layer of the olfactory bulb
│           │       │       ├── Granule cell layer of the accessory olfactory bulb
│           │       │       ├── Granule cell layer of the olfactory bulb
│           │       │       ├── Internal plexiform layer of the olfactory bulb
│           │       │       ├── Mitral cell layer of the accessory olfactory bulb
│           │       │       ├── Mitral cell layer of the olfactory bulb
│           │       │       └── Olfactory nerve layer
│           │       └── SEPTUM
│           │           ├── Lambdoid spetal zone
│           │           ├── Lateral nucleus of the diagonal band
│           │           ├── Lateral septal nuclei
│           │           │   ├── Lateral septal nucleus; intermediate part
│           │           │   ├── Lateral septal nucleus; ventral part
│           │           │   └── Lateral septal nucleus;dorsal part
│           │           ├── Medial septal nucleus
│           │           ├── Nucleus of the horizontal limb of the diagonal band
│           │           ├── Nucleus of the vertical limb of the diagonal band
│           │           ├── Paradiagonal zone
│           │           ├── Septofimbrial nucleus
│           │           ├── Septohippocampal nucleus
│           │           └── Triangular septal nucleus
│           ├── SULCUS
│           │   ├── Calcarine sulcus
│           │   ├── Hippocampal fissure
│           │   ├── Intraparietal sulcus
│           │   ├── Lateral fissure
│           │   ├── Occipitotemporal sulcus
│           │   ├── Orbital sulcus
│           │   ├── Posterolateral fissure
│           │   ├── Preculminate fissure
│           │   ├── Prepyramidal fissure
│           │   ├── Primary fissure
│           │   ├── Rhinal fissure
│           │   ├── Secondary fissure
│           │   ├── Superior temporal sulcus
│           │   └── Ventromedian fissure
│           ├── SURFACE
│           └── VENTRICLE
│               ├── Aqueduct
│               ├── Central canal
│               ├── Dorsal 3rd ventricle
│               ├── Fourth ventricle
│               ├── Interventricular foramen
│               ├── Lateral recess of the 4th ventricle
│               ├── Lateral ventricle
│               ├── Mammillary recess of the 3rd ventricle
│               ├── Recess of the inferior colliculus
│               └── Third ventricle
├── Neck
└── Trunk
```
<!-- HIERARCHY_END -->

## Relationships

<!-- MERMAID_START -->
<!-- MERMAID_END -->

<!-- TABLES_START -->
<!-- TABLES_END -->

## Getting Started

### Add Structures via Issue Templates

1. Go to [Issues → New Issue](../../issues/new/choose)
2. Select **"➕ Add New Structure"**
3. Fill out the form and submit
4. Wait for approval and automatic PR creation

### Local Development

```bash
# Clone and setup
git clone <this-repo>
cd bap-ontology-marmoset

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Validate
python scripts/validate.py

# Generate OWL
python scripts/generate_owl.py --output bap-marmoset.owl
```

## Repository Structure

```
bap-ontology-marmoset/
├── structures/           # Anatomical structure definitions
│   ├── body_regions.yaml # Base hierarchy
│   ├── muscles.yaml      # Muscle structures
│   ├── nerves.yaml       # Nerve structures
│   ├── vessels.yaml      # Blood vessel structures
│   └── skeletal.yaml     # Bone structures
├── relationships/        # Cross-structure relationships
│   ├── innervation.yaml  # Nerve → muscle connections
│   ├── blood_supply.yaml # Vessel → structure connections
│   └── developmental.yaml# Developmental origins
├── schemas/              # JSON Schema for validation
├── scripts/              # Build and validation scripts
└── .github/workflows/    # CI/CD automation
```

## Contributing

1. Create a feature branch from `main`
2. Make your changes to YAML files
3. Run `python scripts/validate.py` locally
4. Open a Pull Request
5. Address review feedback
6. Merge after approval

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Brain Architecture Project
