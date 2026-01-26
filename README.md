# BAP Mouse Head Ontology

A collaborative repository for managing the Brain Architecture Project (BAP) mouse head anatomical ontology.

## 📚 [**View the Auto-Generated Wiki →**](https://mitralab-organization.github.io/bap-ontology-editor/)

Complete documentation with detailed reports, statistics, and visualizations - **automatically updated on every push!**

## Overview

This repository provides a human-readable way to manage:
- **Anatomical structures** (muscles, nerves, blood vessels)
- **Hierarchies** (parent-child relationships)
- **Biological relationships** (innervation, blood supply, developmental origins)

Changes are validated automatically via GitHub Actions and generate OWL files for use in WebProtégé and other tools.

<!-- STATS_START -->
📊 **Ontology Statistics**
```
├── Structures: 395
├── Hierarchy depth: 7 levels
└── Relationships: 75
    ├── Innervated By: 68
    ├── Part Of: 3
    └── Supplied By: 4
```
<!-- STATS_END -->

## Current Hierarchy

<!-- HIERARCHY_START -->
```
Body
├── Appendages
│   ├── Forelimb
│   │   ├── clavicle (L)
│   │   ├── clavicle (R)
│   │   ├── scapula (L)
│   │   └── scapula (R)
│   ├── Hindlimb (L)
│   ├── Hindlimb (R)
│   └── Tail
├── Head
│   ├── Cavities and passages
│   │   ├── Ear Cavities
│   │   │   ├── external acoustic meatus (L)
│   │   │   ├── external acoustic meatus (R)
│   │   │   ├── internal acoustic meatus (L)
│   │   │   └── internal acoustic meatus (R)
│   │   ├── Nasal cavity
│   │   ├── Oral cavity
│   │   ├── Paranasal sinuses (L)
│   │   └── Paranasal sinuses (R)
│   ├── Endocrine and exocrine system
│   │   ├── Palatal submucosa (L)
│   │   ├── Palatal submucosa (R)
│   │   ├── Parotid glands (L)
│   │   └── Parotid glands (R)
│   ├── Integumentary system
│   │   ├── External ear
│   │   │   ├── Pinna (L)
│   │   │   └── Pinna (R)
│   │   ├── Skin (L)
│   │   ├── Skin (R)
│   │   ├── Whiskers (L)
│   │   └── Whiskers (R)
│   ├── Musculoskeletal system
│   │   ├── Cranial muscles
│   │   │   ├── Buccinatorius
│   │   │   │   ├── Buccinatorius (L)
│   │   │   │   └── Buccinatorius (R)
│   │   │   ├── Ceratohyoideus (L)
│   │   │   ├── Ceratohyoideus (R)
│   │   │   ├── Depressor rhinarii
│   │   │   │   ├── Depressor rhinarii (L)
│   │   │   │   └── Depressor rhinarii (R)
│   │   │   ├── Depressor septi nasi
│   │   │   │   ├── Depressor septi nasi (L)
│   │   │   │   └── Depressor septi nasi (R)
│   │   │   ├── Digastricus anterior
│   │   │   │   ├── Digastricus anterior (L)
│   │   │   │   └── Digastricus anterior (R)
│   │   │   ├── Digastricus posterior
│   │   │   │   ├── Digastricus posterior (L)
│   │   │   │   └── Digastricus posterior (R)
│   │   │   ├── Dilatator nasi
│   │   │   │   ├── Dilatator nasi (L)
│   │   │   │   └── Dilatator nasi (R)
│   │   │   ├── External Ear Muscles
│   │   │   │   ├── Auricularis anterior (L)
│   │   │   │   ├── Auricularis anterior (R)
│   │   │   │   ├── Auricularis posterior (L)
│   │   │   │   ├── Auricularis posterior (R)
│   │   │   │   ├── Auricularis superior (L)
│   │   │   │   └── Auricularis superior (R)
│   │   │   ├── Eye Muscles
│   │   │   │   ├── inferior oblique (L)
│   │   │   │   ├── inferior oblique (R)
│   │   │   │   ├── lateral rectus (L)
│   │   │   │   ├── lateral rectus (R)
│   │   │   │   ├── levator palpebrae superioris (L)
│   │   │   │   ├── levator palpebrae superioris (R)
│   │   │   │   ├── medial rectus (L)
│   │   │   │   ├── medial rectus (R)
│   │   │   │   ├── retractor bulbi (L)
│   │   │   │   ├── retractor bulbi (R)
│   │   │   │   ├── superior oblique muscle
│   │   │   │   │   └── superior oblique tendon
│   │   │   │   │       ├── trochlea (L)
│   │   │   │   │       └── trochlea (R)
│   │   │   │   ├── superior rectus (L)
│   │   │   │   └── superior rectus (R)
│   │   │   ├── Frontalis (L)
│   │   │   ├── Frontalis (R)
│   │   │   ├── Geniohyoideus (L)
│   │   │   ├── Geniohyoideus (R)
│   │   │   ├── Inner Ear Muscles
│   │   │   │   ├── Stapedius
│   │   │   │   │   ├── Stapedius (L)
│   │   │   │   │   └── Stapedius (R)
│   │   │   │   ├── Tensor tympani (L)
│   │   │   │   └── Tensor tympani (R)
│   │   │   ├── Interscutularis
│   │   │   │   ├── Interscutularis (L)
│   │   │   │   └── Interscutularis (R)
│   │   │   ├── Levator anguli oris
│   │   │   │   ├── Levator anguli oris (L)
│   │   │   │   └── Levator anguli oris (R)
│   │   │   ├── Levator labii superioris
│   │   │   │   ├── Levator labii superioris (L)
│   │   │   │   └── Levator labii superioris (R)
│   │   │   ├── Levator labii superioris alaeque nasi
│   │   │   │   ├── Levator labii superioris alaeque nasi (L)
│   │   │   │   └── Levator labii superioris alaeque nasi (R)
│   │   │   ├── Levator rhinarii
│   │   │   │   ├── Levator rhinarii (L)
│   │   │   │   └── Levator rhinarii (R)
│   │   │   ├── Mandibuloauricularis
│   │   │   │   ├── Mandibuloauricularis (L)
│   │   │   │   └── Mandibuloauricularis (R)
│   │   │   ├── Masseter
│   │   │   │   ├── Deep masseter
│   │   │   │   │   ├── Deep masseter (L)
│   │   │   │   │   └── Deep masseter (R)
│   │   │   │   ├── Superficial masseter
│   │   │   │   │   ├── Superficial masseter (L)
│   │   │   │   │   └── Superficial masseter (R)
│   │   │   │   └── Zygomaticomandibularis
│   │   │   │       ├── Zygomaticomandibularis (L)
│   │   │   │       └── Zygomaticomandibularis (R)
│   │   │   ├── Mylohyoideus
│   │   │   │   ├── Mylohyoideus (L)
│   │   │   │   └── Mylohyoideus (R)
│   │   │   ├── Nasalis
│   │   │   │   ├── Nasalis (L)
│   │   │   │   └── Nasalis (R)
│   │   │   ├── Occipitalis
│   │   │   │   ├── Occipitalis (L)
│   │   │   │   └── Occipitalis (R)
│   │   │   ├── Orbicularis oculi
│   │   │   │   ├── Orbicularis oculi (L)
│   │   │   │   └── Orbicularis oculi (R)
│   │   │   ├── Orbicularis oris
│   │   │   ├── Orbito-temporo-auricularis
│   │   │   │   ├── Orbito-temporo-auricularis (L)
│   │   │   │   └── Orbito-temporo-auricularis (R)
│   │   │   ├── Platysma cervicale
│   │   │   │   ├── Platysma cervicale (L)
│   │   │   │   └── Platysma cervicale (R)
│   │   │   ├── Platysma myoides
│   │   │   │   ├── Platysma myoides (L)
│   │   │   │   └── Platysma myoides (R)
│   │   │   ├── Pterygoideus lateralis
│   │   │   │   ├── Pterygoideus lateralis (L)
│   │   │   │   └── Pterygoideus lateralis (R)
│   │   │   ├── Pterygoideus medialis
│   │   │   │   ├── Pterygoideus medialis (L)
│   │   │   │   └── Pterygoideus medialis (R)
│   │   │   ├── Sphincter colli profundus
│   │   │   │   ├── Sphincter colli profundus (L)
│   │   │   │   └── Sphincter colli profundus (R)
│   │   │   ├── Sphincter colli superficialis
│   │   │   │   ├── Sphincter colli superficialis (L)
│   │   │   │   └── Sphincter colli superficialis (R)
│   │   │   ├── Sternohyoideus (L)
│   │   │   ├── Sternohyoideus (R)
│   │   │   ├── Stylohyoideus
│   │   │   │   ├── Stylohyoideus (L)
│   │   │   │   └── Stylohyoideus (R)
│   │   │   ├── Stylopharyngeus
│   │   │   │   ├── Stylopharyngeus (L)
│   │   │   │   └── Stylopharyngeus (R)
│   │   │   ├── Temporalis
│   │   │   │   ├── Temporalis lateralis (L)
│   │   │   │   ├── Temporalis lateralis (R)
│   │   │   │   ├── Temporalis medialis (L)
│   │   │   │   └── Temporalis medialis (R)
│   │   │   ├── Tongue muscles
│   │   │   │   ├── Extrinsic tongue muscles
│   │   │   │   │   ├── Genioglossus
│   │   │   │   │   │   ├── Genioglossus (L)
│   │   │   │   │   │   └── Genioglossus (R)
│   │   │   │   │   ├── Hyoglossus
│   │   │   │   │   │   ├── Hyoglossus (L)
│   │   │   │   │   │   └── Hyoglossus (R)
│   │   │   │   │   ├── Palatoglossus (L)
│   │   │   │   │   ├── Palatoglossus (R)
│   │   │   │   │   ├── Styloglossus (L)
│   │   │   │   │   └── Styloglossus (R)
│   │   │   │   └── Intrinsic tongue muscles
│   │   │   │       ├── Inferior longitudinal (L)
│   │   │   │       ├── Inferior longitudinal (R)
│   │   │   │       ├── Superior longitudinal (L)
│   │   │   │       ├── Superior longitudinal (R)
│   │   │   │       ├── Transverse (L)
│   │   │   │       ├── Transverse (R)
│   │   │   │       ├── Vertical (L)
│   │   │   │       └── Vertical (R)
│   │   │   ├── Zygomaticus major
│   │   │   │   ├── Zygomaticus major (L)
│   │   │   │   └── Zygomaticus major (R)
│   │   │   └── Zygomaticus minor
│   │   │       ├── Zygomaticus minor (L)
│   │   │       └── Zygomaticus minor (R)
│   │   └── Cranium
│   │       ├── Inner ear
│   │       │   ├── incus (L)
│   │       │   ├── incus (R)
│   │       │   ├── malleus (L)
│   │       │   ├── malleus (R)
│   │       │   ├── stapes (L)
│   │       │   └── stapes (R)
│   │       ├── Neurocranium
│   │       │   ├── basisphenoid (L)
│   │       │   ├── basisphenoid (R)
│   │       │   ├── ethmoid (L)
│   │       │   ├── ethmoid (R)
│   │       │   ├── frontal
│   │       │   ├── interparietal (L)
│   │       │   ├── interparietal (R)
│   │       │   ├── occipital
│   │       │   ├── parietal (L)
│   │       │   ├── parietal (R)
│   │       │   ├── presphenoid (L)
│   │       │   ├── presphenoid (R)
│   │       │   ├── tympanic membrane (L)
│   │       │   └── tympanic membrane (R)
│   │       └── Viscerocranium
│   │           ├── Jaw apparatus
│   │           │   ├── mandible (L)
│   │           │   ├── mandible (R)
│   │           │   ├── maxilla (L)
│   │           │   └── maxilla (R)
│   │           ├── lacrimal (L)
│   │           ├── lacrimal (R)
│   │           ├── nasal (L)
│   │           ├── nasal (R)
│   │           ├── palatine (L)
│   │           ├── palatine (R)
│   │           ├── premaxilla (L)
│   │           ├── premaxilla (R)
│   │           ├── sphenoid
│   │           ├── squamosal (L)
│   │           ├── squamosal (R)
│   │           ├── vomer
│   │           ├── zygomatic (L)
│   │           └── zygomatic (R)
│   ├── Nervous system
│   │   ├── Central nervous system
│   │   │   └── Brain
│   │   └── Peripheral nervous system
│   │       └── Cranial Nerves
│   │           ├── Abducens nerve (L)
│   │           ├── Abducens nerve (R)
│   │           ├── Accessory nerve
│   │           │   ├── Accessory nerve (L)
│   │           │   └── Accessory nerve (R)
│   │           ├── Facial nerve
│   │           │   ├── Facial nerve (L)
│   │           │   └── Facial nerve (R)
│   │           ├── Glossopharyngeal nerve
│   │           │   ├── Glossopharyngeal nerve (L)
│   │           │   └── Glossopharyngeal nerve (R)
│   │           ├── Hypoglossal nerve
│   │           │   ├── Hypoglossal nerve (L)
│   │           │   └── Hypoglossal nerve (R)
│   │           ├── Oculomotor nerve (L)
│   │           ├── Oculomotor nerve (R)
│   │           ├── Olfactory nerve (L)
│   │           ├── Olfactory nerve (R)
│   │           ├── Optic nerve (L)
│   │           ├── Optic nerve (R)
│   │           ├── Terminal nerve (L)
│   │           ├── Terminal nerve (R)
│   │           ├── Trigeminal nerve
│   │           │   ├── Trigeminal nerve (L)
│   │           │   └── Trigeminal nerve (R)
│   │           ├── Trochlear nerve (L)
│   │           ├── Trochlear nerve (R)
│   │           ├── Vagus nerve (L)
│   │           ├── Vagus nerve (R)
│   │           ├── Vestibulocochlear nerve (L)
│   │           └── Vestibulocochlear nerve (R)
│   ├── Sense organs
│   │   ├── Eye (L)
│   │   ├── Eye (R)
│   │   ├── Gustatory epithelium (L)
│   │   ├── Gustatory epithelium (R)
│   │   ├── Inner ear (L)
│   │   ├── Inner ear (R)
│   │   ├── Olfactory epithelium (L)
│   │   ├── Olfactory epithelium (R)
│   │   ├── Whisker barrels (L)
│   │   └── Whisker barrels (R)
│   └── Vascular system
│       ├── Arteries
│       │   ├── Lingual artery
│       │   │   ├── Lingual artery (L)
│       │   │   └── Lingual artery (R)
│       │   ├── Maxillary artery
│       │   │   ├── Maxillary artery (L)
│       │   │   └── Maxillary artery (R)
│       │   └── Temporal artery
│       │       ├── Temporal artery (L)
│       │       └── Temporal artery (R)
│       ├── Lymphatics (L)
│       ├── Lymphatics (R)
│       ├── Veins (L)
│       └── Veins (R)
├── Neck
│   ├── Cavities and passages
│   │   ├── Larynx
│   │   └── Pharynx
│   │       ├── Esophagus
│   │       ├── sternofacialis left (L)
│   │       └── sternofacialis left (R)
│   ├── Endocrine and exocrine system
│   │   └── Thyroid gland
│   ├── Integumentary system
│   │   ├── Skin (L)
│   │   └── Skin (R)
│   ├── Musculoskeletal system
│   │   ├── Neck muscles
│   │   │   ├── Cleidomastoideus (L)
│   │   │   ├── Cleidomastoideus (R)
│   │   │   ├── Cleidooccipitalis (L)
│   │   │   ├── Cleidooccipitalis (R)
│   │   │   ├── Cricothyroideus (L)
│   │   │   ├── Cricothyroideus (R)
│   │   │   ├── Jugulohyoideus (L)
│   │   │   ├── Jugulohyoideus (R)
│   │   │   ├── Laryngeal muscles
│   │   │   │   ├── Arytenoideus (L)
│   │   │   │   ├── Arytenoideus (R)
│   │   │   │   ├── Cricoarytenoideus alaris (L)
│   │   │   │   ├── Cricoarytenoideus alaris (R)
│   │   │   │   ├── Cricoarytenoideus lateralis (L)
│   │   │   │   ├── Cricoarytenoideus lateralis (R)
│   │   │   │   ├── Cricoarytenoideus posterior (L)
│   │   │   │   ├── Cricoarytenoideus posterior (R)
│   │   │   │   ├── Thyroarytenoideus (L)
│   │   │   │   └── Thyroarytenoideus (R)
│   │   │   ├── Omohyoideus (L)
│   │   │   ├── Omohyoideus (R)
│   │   │   ├── Pharyngeal muscles
│   │   │   │   ├── Constrictor pharyngis inferior (L)
│   │   │   │   ├── Constrictor pharyngis inferior (R)
│   │   │   │   ├── Constrictor pharyngis medius (L)
│   │   │   │   ├── Constrictor pharyngis medius (R)
│   │   │   │   ├── Constrictor pharyngis superior (L)
│   │   │   │   ├── Constrictor pharyngis superior (R)
│   │   │   │   ├── Levator veli palatini (L)
│   │   │   │   ├── Levator veli palatini (R)
│   │   │   │   ├── Palatopharyngeus (L)
│   │   │   │   ├── Palatopharyngeus (R)
│   │   │   │   ├── Pterygopharyngeus (L)
│   │   │   │   ├── Pterygopharyngeus (R)
│   │   │   │   ├── Salpingopharyngeus (L)
│   │   │   │   ├── Salpingopharyngeus (R)
│   │   │   │   └── Tensor veli palatini
│   │   │   │       ├── Tensor veli palatini (L)
│   │   │   │       └── Tensor veli palatini (R)
│   │   │   ├── Sternomastoideus (L)
│   │   │   ├── Sternomastoideus (R)
│   │   │   ├── Sternothyroideus (L)
│   │   │   ├── Sternothyroideus (R)
│   │   │   ├── Thyrohyoideus (L)
│   │   │   ├── Thyrohyoideus (R)
│   │   │   └── Trapezius
│   │   │       ├── Acromiotrapezius (L)
│   │   │       ├── Acromiotrapezius (R)
│   │   │       ├── Spinotrapezius (L)
│   │   │       └── Spinotrapezius (R)
│   │   └── Neck skeletal system
│   │       ├── Laryngeal skeletal system
│   │       │   ├── arytenoid cartilage (L)
│   │       │   ├── arytenoid cartilage (R)
│   │       │   ├── cricoid cartilage (L)
│   │       │   ├── cricoid cartilage (R)
│   │       │   ├── epiglottis
│   │       │   ├── laryngeal alar cartilage (L)
│   │       │   ├── laryngeal alar cartilage (R)
│   │       │   └── thyroid cartilage
│   │       ├── Pharyngeal skeleton
│   │       │   └── hyoid bone
│   │       └── cervical vertebra
│   ├── Nervous system
│   │   ├── Central nervous system
│   │   │   └── Spinal Cord
│   │   └── Peripheral nervous system
│   │       ├── Cervical nerves (L)
│   │       └── Cervical nerves (R)
│   └── Vascular system
│       ├── Arteries (L)
│       ├── Arteries (R)
│       ├── Lymphatics (L)
│       ├── Lymphatics (R)
│       ├── Veins (L)
│       └── Veins (R)
└── Trunk
    ├── Abdomen (L)
    ├── Abdomen (R)
    ├── Pelvis (L)
    ├── Pelvis (R)
    └── Thorax
        ├── sternum (L)
        └── sternum (R)
```
<!-- HIERARCHY_END -->

## Relationships

<!-- MERMAID_START -->
#### Innervation Map
```mermaid
graph LR
    Facial_nerve_(L)[Facial nerve (L)]
    Facial_nerve_(L) -->|innervates| Buccinatorius_(L)[Buccinatorius (L)]
    Facial_nerve_(L) -->|innervates| Depressor_rhinarii_(L)[Depressor rhinarii (L)]
    Facial_nerve_(L) -->|innervates| Depressor_septi_nasi_(L)[Depressor septi nasi (L)]
    Facial_nerve_(L) -->|innervates| Digastricus_posterior_(L)[Digastricus posterior (L)]
    Facial_nerve_(L) -->|innervates| Dilatator_nasi_(L)[Dilatator nasi (L)]
    Facial_nerve_(L) -->|innervates| Interscutularis_(L)[Interscutularis (L)]
    Facial_nerve_(L) -->|innervates| Levator_anguli_oris_(L)[Levator anguli oris (L)]
    Facial_nerve_(L) -->|innervates| Levator_labii_superioris_(L)[Levator labii superioris (L)]
    Facial_nerve_(L) -->|innervates| Facial_nerve_(L)_more[+15 more]
    Facial_nerve_(R)[Facial nerve (R)]
    Facial_nerve_(R) -->|innervates| Buccinatorius_(R)[Buccinatorius (R)]
    Facial_nerve_(R) -->|innervates| Depressor_rhinarii_(R)[Depressor rhinarii (R)]
    Facial_nerve_(R) -->|innervates| Depressor_septi_nasi_(R)[Depressor septi nasi (R)]
    Facial_nerve_(R) -->|innervates| Digastricus_posterior_(R)[Digastricus posterior (R)]
    Facial_nerve_(R) -->|innervates| Dilatator_nasi_(R)[Dilatator nasi (R)]
    Facial_nerve_(R) -->|innervates| Interscutularis_(R)[Interscutularis (R)]
    Facial_nerve_(R) -->|innervates| Levator_anguli_oris_(R)[Levator anguli oris (R)]
    Facial_nerve_(R) -->|innervates| Levator_labii_superioris_(R)[Levator labii superioris (R)]
    Facial_nerve_(R) -->|innervates| Facial_nerve_(R)_more[+15 more]
    Glossopharyngeal_nerve_(L)[Glossopharyngeal nerve (L)]
    Glossopharyngeal_nerve_(L) -->|innervates| Stylopharyngeus_(L)[Stylopharyngeus (L)]
    Glossopharyngeal_nerve_(R)[Glossopharyngeal nerve (R)]
    Glossopharyngeal_nerve_(R) -->|innervates| Stylopharyngeus_(R)[Stylopharyngeus (R)]
    Hypoglossal_nerve_(L)[Hypoglossal nerve (L)]
    Hypoglossal_nerve_(L) -->|innervates| Genioglossus_(L)[Genioglossus (L)]
    Hypoglossal_nerve_(L) -->|innervates| Hyoglossus_(L)[Hyoglossus (L)]
    Hypoglossal_nerve_(R)[Hypoglossal nerve (R)]
    Hypoglossal_nerve_(R) -->|innervates| Genioglossus_(R)[Genioglossus (R)]
    Hypoglossal_nerve_(R) -->|innervates| Hyoglossus_(R)[Hyoglossus (R)]
    Trigeminal_nerve_(L)[Trigeminal nerve (L)]
    Trigeminal_nerve_(L) -->|innervates| Deep_masseter_(L)[Deep masseter (L)]
    Trigeminal_nerve_(L) -->|innervates| Digastricus_anterior_(L)[Digastricus anterior (L)]
    Trigeminal_nerve_(L) -->|innervates| Mylohyoideus_(L)[Mylohyoideus (L)]
    Trigeminal_nerve_(L) -->|innervates| Pterygoideus_lateralis_(L)[Pterygoideus lateralis (L)]
    Trigeminal_nerve_(L) -->|innervates| Pterygoideus_medialis_(L)[Pterygoideus medialis (L)]
    Trigeminal_nerve_(L) -->|innervates| Superficial_masseter_(L)[Superficial masseter (L)]
    Trigeminal_nerve_(L) -->|innervates| Tensor_veli_palatini_(L)[Tensor veli palatini (L)]
    Trigeminal_nerve_(L) -->|innervates| Zygomaticomandibularis_(L)[Zygomaticomandibularis (L)]
    Trigeminal_nerve_(R)[Trigeminal nerve (R)]
    Trigeminal_nerve_(R) -->|innervates| Deep_masseter_(R)[Deep masseter (R)]
    Trigeminal_nerve_(R) -->|innervates| Digastricus_anterior_(R)[Digastricus anterior (R)]
    Trigeminal_nerve_(R) -->|innervates| Mylohyoideus_(R)[Mylohyoideus (R)]
    Trigeminal_nerve_(R) -->|innervates| Pterygoideus_lateralis_(R)[Pterygoideus lateralis (R)]
    Trigeminal_nerve_(R) -->|innervates| Pterygoideus_medialis_(R)[Pterygoideus medialis (R)]
    Trigeminal_nerve_(R) -->|innervates| Superficial_masseter_(R)[Superficial masseter (R)]
    Trigeminal_nerve_(R) -->|innervates| Tensor_veli_palatini_(R)[Tensor veli palatini (R)]
    Trigeminal_nerve_(R) -->|innervates| Zygomaticomandibularis_(R)[Zygomaticomandibularis (R)]
```

#### Blood Supply Map
```mermaid
graph LR
    Lingual_artery_L([Lingual artery (L)])
    Lingual_artery_L -.->|supplies| Genioglossus_L[Genioglossus (L)]
    Lingual_artery_L -.->|supplies| Hyoglossus_L[Hyoglossus (L)]
    Lingual_artery_R([Lingual artery (R)])
    Lingual_artery_R -.->|supplies| Genioglossus_R[Genioglossus (R)]
    Lingual_artery_R -.->|supplies| Hyoglossus_R[Hyoglossus (R)]
```
<!-- MERMAID_END -->

<!-- TABLES_START -->
### Innervation

| Nerve | Innervates |
|-------|------------|
| Facial nerve (L) | Buccinatorius (L), Depressor rhinarii (L), Depressor septi nasi (L), Digastricus posterior (L), Dilatator nasi (L), Interscutularis (L), Levator anguli oris (L), Levator labii superioris (L), Levator labii superioris alaeque nasi (L), Levator rhinarii (L), Mandibuloauricularis (L), Nasalis (L), Occipitalis (L), Orbicularis oculi (L), Orbito-temporo-auricularis (L), Platysma cervicale (L), Platysma myoides (L), Sphincter colli profundus (L), Sphincter colli superficialis (L), Stapedius (L), Stylohyoideus (L), Zygomaticus major (L), Zygomaticus minor (L) |
| Facial nerve (R) | Buccinatorius (R), Depressor rhinarii (R), Depressor septi nasi (R), Digastricus posterior (R), Dilatator nasi (R), Interscutularis (R), Levator anguli oris (R), Levator labii superioris (R), Levator labii superioris alaeque nasi (R), Levator rhinarii (R), Mandibuloauricularis (R), Nasalis (R), Occipitalis (R), Orbicularis oculi (R), Orbito-temporo-auricularis (R), Platysma cervicale (R), Platysma myoides (R), Sphincter colli profundus (R), Sphincter colli superficialis (R), Stapedius (R), Stylohyoideus (R), Zygomaticus major (R), Zygomaticus minor (R) |
| Glossopharyngeal nerve (L) | Stylopharyngeus (L) |
| Glossopharyngeal nerve (R) | Stylopharyngeus (R) |
| Hypoglossal nerve (L) | Genioglossus (L), Hyoglossus (L) |
| Hypoglossal nerve (R) | Genioglossus (R), Hyoglossus (R) |
| Trigeminal nerve (L) | Deep masseter (L), Digastricus anterior (L), Mylohyoideus (L), Pterygoideus lateralis (L), Pterygoideus medialis (L), Superficial masseter (L), Tensor veli palatini (L), Zygomaticomandibularis (L) |
| Trigeminal nerve (R) | Deep masseter (R), Digastricus anterior (R), Mylohyoideus (R), Pterygoideus lateralis (R), Pterygoideus medialis (R), Superficial masseter (R), Tensor veli palatini (R), Zygomaticomandibularis (R) |

### Blood Supply

| Artery | Supplies |
|--------|----------|
| Lingual artery (L) | Genioglossus (L), Hyoglossus (L) |
| Lingual artery (R) | Genioglossus (R), Hyoglossus (R) |
<!-- TABLES_END -->

## Repository Structure

```
bap-ontology/
├── structures/           # Anatomical structure definitions
│   ├── muscles.yaml      # Muscle structures + hierarchies
│   ├── nerves.yaml       # Nerve structures
│   └── vessels.yaml      # Blood vessel structures
├── relationships/        # Cross-structure relationships
│   ├── innervation.yaml  # Nerve → muscle connections
│   ├── blood_supply.yaml # Vessel → structure connections
│   └── developmental.yaml# Developmental origins
├── schemas/              # JSON Schema for validation
│   └── structure.schema.json
├── scripts/              # Build and validation scripts
│   ├── validate.py       # Validate YAML files
│   ├── generate_owl.py   # Generate OWL from YAML
│   ├── generate_tree.py  # Generate hierarchy tree
│   └── process_*.py      # Issue processors
└── .github/workflows/    # CI/CD automation
    ├── validate.yml      # Validate on PR
    └── generate.yml      # Generate OWL on merge
```

## 🎯 Easy Way: Use Issue Templates (Recommended)

**No coding required!** Just fill out a form to propose changes:

### Add a New Structure

1. Go to [Issues → New Issue](../../issues/new/choose)
2. Select **"➕ Add New Structure"**
3. Fill out the form:
   - Structure name
   - Body region (Head, Neck, Trunk, Appendages)
   - Organ system
   - Parent structure
   - Definition
4. Submit the issue
5. A maintainer reviews and adds the `approved` label
6. 🤖 A PR is automatically created with the YAML changes!

### Add a New Relationship

1. Go to [Issues → New Issue](../../issues/new/choose)
2. Select **"🔗 Add New Relationship"**
3. Fill out the form:
   - Relationship type (innervation, blood supply, etc.)
   - Subject structure (e.g., the muscle)
   - Object structure (e.g., the nerve)
   - Confidence level
   - References
4. Submit and wait for approval

### Modify Hierarchy

Use the **"📁 Modify Hierarchy"** template to propose moving structures to different parents.

---

## 💻 Developer Way: Direct YAML Editing

For power users who prefer editing files directly:

### 1. Clone the repository

```bash
git clone https://github.com/MitraLab-Organization/bap-ontology-editor.git
cd bap-ontology-editor
```

### 2. Edit structures

Edit YAML files directly in `structures/` or `relationships/`:

```yaml
# structures/muscles.yaml
structures:
  - id: BAP_0001000
    name: Head muscle
    parent: null  # Root structure
    definition: Muscles of the head region

  - id: BAP_0001100
    name: Masseter
    parent: BAP_0001000
    definition: Primary muscle of mastication
    abbreviation: MAS
```

### 3. Create a Pull Request

1. Create a branch: `git checkout -b add-temporalis-muscle`
2. Make your changes
3. Push and open a PR
4. GitHub Actions validates your changes
5. Get review and merge

### 4. Generated OWL file

After merge, the `bap-mousehead.owl` file is automatically generated and available in the releases.

## YAML Format Reference

### Structure Definition

```yaml
structures:
  - id: BAP_0000001          # Required: Unique IRI identifier
    name: Structure Name      # Required: Human-readable name
    parent: BAP_0000000       # Optional: Parent structure ID (null for roots)
    definition: Description   # Optional: IAO definition text
    abbreviation: ABBR        # Optional: Short form
    external_id: UBERON_0001  # Optional: Cross-reference to external ontology
```

### Relationship Definition

```yaml
relationships:
  - subject: BAP_0001100      # Required: Source structure ID
    predicate: innervated_by  # Required: Relationship type
    object: BAP_0002001       # Required: Target structure ID
    reference: PMID:12345     # Optional: Citation
```

### Supported Relationship Types

| Predicate | OBO IRI | Description |
|-----------|---------|-------------|
| `part_of` | BFO_0000050 | Structure is part of another |
| `innervated_by` | RO_0002005 | Receives neural input from |
| `supplied_by` | RO_0002178 | Receives blood supply from |
| `develops_from` | RO_0002202 | Developmental origin |
| `adjacent_to` | RO_0002220 | Spatially contiguous |

## Local Development

### Prerequisites

- Python 3.9+
- PyYAML, jsonschema

### Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Validate locally

```bash
python scripts/validate.py
```

### Generate OWL locally

```bash
python scripts/generate_owl.py --output bap-mousehead.owl
```

## Access Control

This repository uses GitHub's built-in access controls:

- **Collaborators**: Can push branches and create PRs
- **Branch protection**: Main branch requires PR reviews
- **CODEOWNERS**: Specific reviewers for critical files

To request access, contact the repository administrators.

## Contributing

1. Create a feature branch from `main`
2. Make your changes to YAML files
3. Run `python scripts/validate.py` locally
4. Open a Pull Request
5. Address review feedback
6. Merge after approval

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) - Brain Architecture Project
