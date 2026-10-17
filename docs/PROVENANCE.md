# Provenance and repository boundaries

This initial standalone Akor repository retains the **read-only** mission preflight behavior from the previously validated `Ekole_Pont_Missions_v4_1` archive. The compiler delegates mission validation to Kontexte and preview preparation to kompose; it delegates scenario schema checks to Orgo's existing injector and world boundary checks to Orgo_Worlds.

No six-repository source code, world data, or student records are copied into Akor. The English wiki was prepared as a documentation companion. The original multiplication mismatch remains visible and unresolved: Kontexte's `boulangerie` source references `qc-pri-ma-006`, whereas the proposed Grade 3 multiplication pilot targets `qc-pri-ma-008`. The repo does not silently change educational claims.

The runtime integration described in the wiki is an **intended future architecture**. The only executable features currently shipped are non-mutating review and preflight checks.
