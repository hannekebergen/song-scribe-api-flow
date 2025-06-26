
# Suno.ai Prompting Cheat Sheet

Welkom bij de ultieme gids voor het prompten in Suno.ai! Deze cheat sheet is ontworpen om je te helpen Nederlandstalige songs precies naar wens te genereren, door alle relevante informatie op één plek te bundelen. Laten we beginnen!




## 1. Styles-systeem

Het Styles-systeem in Suno.ai is cruciaal voor het sturen van de muzikale output. Styles bepalen het genre, de sfeer en de instrumentatie van je nummer. Door de juiste styles te kiezen, zorg je ervoor dat Suno.ai een song genereert die past bij jouw visie.

### Hoofdgenres (minimaal 20)

*   **Pop:** Algemeen, commercieel, pakkend.
*   **Rock:** Energieke gitaren, drums, bas.
*   **Hip-Hop:** Ritme, rap, beats.
*   **Elektronisch (EDM):** Synthesizers, dance-beats.
*   **R&B:** Soulvolle zang, gladde productie.
*   **Country:** Folk-invloeden, verhalende teksten.
*   **Jazz:** Improvisatie, complexe harmonieën.
*   **Klassiek:** Orchestrale arrangementen.
*   **Blues:** Gevoelvolle zang, gitaarsolo's.
*   **Folk:** Akoestisch, traditionele instrumenten.
*   **Reggae:** Off-beat ritmes, baslijnen.
*   **Metal:** Zware gitaren, agressieve zang.
*   **Punk:** Snelle, rauwe energie.
*   **Disco:** Dansbaar, funky baslijnen.
*   **Funk:** Groovy ritmes, blazers.
*   **Soul:** Gospel-invloeden, emotionele zang.
*   **Latin:** Ritmes uit Latijns-Amerika.
*   **Wereldmuziek:** Diverse culturele invloeden.
*   **Ambient:** Sfeervol, rustgevend.
*   **Soundtrack:** Filmische, orkestrale klanken.

### Substijlen (minimaal 50)

*   **Pop:** Synth-pop, Indie-pop, Dream-pop, Power-pop, Teen-pop, Art-pop, Baroque-pop, Dance-pop, Electropop, J-pop, K-pop, Latin-pop, Nederpop, Pop-rock, Soft-pop, Trap-pop.
*   **Rock:** Hardrock, Alternatieve rock, Indie-rock, Punkrock, Garagerock, Psychedelische rock, Progressieve rock, Glamrock, Bluesrock, Folkrock, Stonerrock, Grunge, Nu-metal, Post-punk, Shoegaze, Surfrock.
*   **Hip-Hop:** Old-school hip-hop, Trap, Boom bap, Gangsta rap, Conscious hip-hop, G-funk, Jazz rap, Lo-fi hip-hop, Mumble rap, UK drill, Crunk, Hyphy, Nerdcore, Political hip-hop, Southern hip-hop, West Coast hip-hop, East Coast hip-hop.
*   **Elektronisch (EDM):** House, Techno, Trance, Dubstep, Drum & Bass, Electro, Chillwave, Synthwave, Future Bass, Trap (EDM), Progressive House, Deep House, Tech House, Hardstyle, Gabber, Breakbeat, IDM, Ambient House, Big Room, Downtempo.
*   **R&B:** Contemporary R&B, Neo-soul, PBR&B, Quiet Storm, New Jack Swing, Soul (modern), Urban Contemporary.
*   **Country:** Americana, Bluegrass, Honky Tonk, Outlaw Country, Nashville Sound, Red Dirt, Western Swing, Folk Country, Pop Country.
*   **Jazz:** Bebop, Cool Jazz, Swing, Fusion, Latin Jazz, Smooth Jazz, Avant-garde Jazz, Dixieland, Free Jazz, Hard Bop, Modal Jazz, Soul Jazz.
*   **Klassiek:** Barok, Romantiek, Modern Klassiek, Impressionisme, Neoclassicisme, Renaissance, Middeleeuws.
*   **Blues:** Delta Blues, Chicago Blues, Electric Blues, Acoustic Blues, Jump Blues, Piedmont Blues, Swamp Blues.
*   **Folk:** Folk-pop, Folk-rock, Indie-folk, Neofolk, Progressive Folk, Psychedelic Folk, Traditional Folk.

### Styles combineren

Je kunt meerdere styles combineren door ze achter elkaar te plaatsen, gescheiden door komma's of spaties. Suno.ai probeert dan elementen van alle opgegeven styles te integreren.

```prompt
[intro][pop, rock, upbeat][language:Dutch]
(Zomerse gitaarriff)
...
```

```prompt
[verse][hip-hop, trap, dark beat][language:Dutch]
(Dreigende synth)
...
```



## 2. Bracket-syntaxis

De juiste toepassing van haakjes is essentieel voor gedetailleerde controle over je Suno.ai generaties. Ze sturen Suno.ai aan over hoe het de tekst moet interpreteren en verwerken.

### [Vierkante haken]

Vierkante haken `[]` worden gebruikt voor muzikale instructies en metadata die niet gezongen moeten worden. Denk hierbij aan:

*   **Sectielabels:** `[intro]`, `[verse]`, `[chorus]`, `[bridge]`, `[outro]`, `[pre-chorus]`, `[post-chorus]`, `[instrumental]`, `[breakdown]`, `[fade out]`, `[solo]`, `[drop]`, `[build-up]`, `[interlude]`, `[coda]`, `[hook]`, `[refrain]`, `[ad-lib]`, `[spoken word]`, `[narration]`, `[dialogue]`, `[vocal chop]`, `[beat switch]`, `[tempo change]`, `[key change]`, `[time signature change]`, `[mood change]`, `[scene change]`, `[sound effect]`, `[silence]`, `[pause]`, `[scream]`, `[whisper]`, `[laugh]`, `[gasp]`, `[cough]`, `[sneeze]`, `[sigh]`, `[grunt]`, `[cheers]`, `[applause]`, `[crowd noise]`, `[radio static]`, `[phone ringing]`, `[door creak]`, `[footsteps]`, `[rain]`, `[thunder]`, `[wind]`, `[ocean waves]`, `[birdsong]`, `[car horn]`, `[siren]`, `[explosion]`, `[gunshot]`, `[glass break]`, `[alarm]`, `[clock ticking]`, `[heartbeat]`, `[camera click]`, `[typewriter]`, `[computer sound]`, `[robot voice]`, `[alien sound]`, `[monster growl]`, `[dragon roar]`, `[magic spell]`, `[sword clank]`, `[bell toll]`, `[chime]`, `[gong]`, `[whistle]`, `[swoosh]`, `[thump]`, `[clatter]`, `[drip]`, `[splash]`, `[crackle]`, `[hiss]`, `[buzz]`, `[hum]`, `[ding]`, `[dong]`, `[click]`, `[clack]`, `[rattle]`, `[jingle]`, `[whoosh]`, `[zap]`, `[boing]`, `[pop]`, `[fizz]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[rattle]`, `[thud]`, `[bang]`, `[clash]`, `[crash]`, `[smash]`, `[thwack]`, `[whack]`, `[swish]`, `[rustle]`, `[crinkle]`, `[snap]`, `[crack]`, `[rip]`, `[tear]`, `[zipper]`, `[velcro]`, `[drip]`, `[splash]`, `[gurgle]`, `[slurp]`, `[chomp]`, `[crunch]`, `[squeak]`, `[creak]`, `[[Vierkante haken]]` voor extra nadruk (indien ondersteund).



### (Ronde haken)

Ronde haken `()` worden gebruikt voor tekst die gezongen moet worden, of voor vocale instructies die de manier van zingen beïnvloeden. Voorbeelden:

*   **Te zingen tekst:** `(Dit is mijn lied)`
*   **Gefluister:** `(fluisterend) Ik hou van jou`
*   **Achtergrondkoor:** `(Achtergrondkoor: Ooh-ooh)`
*   **Layering-trucs:** `(dubbele stem) Ik ben hier`

### Prioriteitsregels

Wanneer je beide typen haken combineert, heeft de context binnen de haakjes voorrang. Instructies in vierkante haken beïnvloeden de algemene muzikale setting, terwijl ronde haken de vocale uitvoering sturen.

```prompt
[verse][upbeat pop] (Zing vrolijk) De zon schijnt vandaag
```

### Gebruik van dubbele haken `[[...]]`

Dubbele vierkante haken `[[...]]` kunnen worden gebruikt om extra nadruk te leggen op een specifieke instructie of stijl. Dit kan Suno.ai helpen om die elementen prominenter te maken in de gegenereerde audio. Gebruik dit spaarzaam voor het beste effect.

```prompt
[chorus][[POWER CHORUS]][rock anthem] (Zing met volle kracht) Wij zijn de kampioenen!
```




### Gebruik van dubbele haken `[[...]]`

Dubbele vierkante haken `[[...]]` kunnen worden gebruikt om extra nadruk te leggen op een specifieke instructie of stijl. Dit kan Suno.ai helpen om die elementen prominenter te maken in de gegenereerde audio. Gebruik dit spaarzaam voor het beste effect.

```prompt
[chorus][[POWER CHORUS]][rock anthem] (Zing met volle kracht) Wij zijn de kampioenen!
```



## 3. Prompt-bouwstenen

Prompt-bouwstenen zijn specifieke tags en parameters die je kunt gebruiken om de muzikale structuur en kenmerken van je nummer te definiëren. Ze bieden gedetailleerde controle over elk aspect van de song.

### Sectietags

Gebruik deze tags om de structuur van je nummer aan te geven. Suno.ai zal de muziek en zang aanpassen aan de typische kenmerken van elke sectie.

*   `[intro]`
*   `[verse]`
*   `[pre-chorus]`
*   `[chorus]`
*   `[bridge]`
*   `[outro]`
*   `[instrumental]`
*   `[breakdown]`
*   `[solo]`

### Muzikale parameters

Deze parameters beïnvloeden de technische aspecten van de muziek.

*   `BPM`: Beats Per Minute. Bepaalt het tempo van het nummer. Bijvoorbeeld: `BPM 120`.
*   `Toonsoort`: De muzikale toonsoort. Bijvoorbeeld: `Toonsoort C majeur` of `Toonsoort Am`.
*   `Maatsoort`: De maatsoort van het nummer. Bijvoorbeeld: `Maatsoort 4/4`.

### Instrumentatie-tags

Specificeer welke instrumenten je wilt horen. Wees zo gedetailleerd mogelijk.

*   `[acoustic guitar]`
*   `[electric guitar]`
*   `[piano]`
*   `[synthesizer]`
*   `[drums]`
*   `[bass]`
*   `[horn section]`
*   `[strings]`
*   `[orchestra]`
*   `[flute]`
*   `[violin]`
*   `[cello]`
*   `[trumpet]`
*   `[saxophone]`
*   `[choir]`

### Vocale descriptors

Beschrijf de gewenste zangstijl of kenmerken van de stem.

*   `[soft female vocal]`
*   `[powerful male vocal]`
*   `[rap flow]`
*   `[spoken word]`
*   `(harmonies)`
*   `(whispering)`
*   `(ad-libs)`
*   `(autotune)`
*   `(vocal effects)`

### Effect-tags

Voeg specifieke audio-effecten toe aan je nummer.

*   `[reverb heavy]`
*   `[lo-fi]`
*   `[8-bit]`
*   `[echo]`
*   `[distortion]`
*   `[delay]`
*   `[chorus effect]`
*   `[flanger]`
*   `[phaser]`
*   `[autotune]`
*   `[vocoder]`
*   `[bitcrusher]`
*   `[tape hiss]`
*   `[vinyl crackle]`
*   `[glitch]`
*   `[sidechain]`
*   `[filter sweep]`



## 4. Voorbeeld-prompts per functie

Hier zijn enkele mini-voorbeelden om specifieke concepten te demonstreren, gevolgd door een uitgebreid 'perfect prompt'.

### Mini-voorbeelden (1 regel)

*   **Genre:**
    ```prompt
    [intro][jazz fusion] (Saxofoon solo begint)
    ```

*   **Instrumentatie:**
    ```prompt
    [verse][acoustic guitar] (Zachte tokkel)
    ```

*   **Vocale stijl:**
    ```prompt
    [chorus][powerful male vocal] (Zing met passie)
    ```

*   **Effect:**
    ```prompt
    [bridge][reverb heavy] (Dromerige klanken)
    ```

*   **Sectie:**
    ```prompt
    [outro] (Langzame fade-out)
    ```

*   **Taal:**
    ```prompt
    [verse][language:Dutch] (Ik loop door de straten)
    ```

*   **BPM:**
    ```prompt
    [intro]BPM 140 (Snelle beat start)
    ```

*   **Toonsoort:**
    ```prompt
    [verse]Toonsoort G majeur (Vrolijke melodie)
    ```

*   **Maatsoort:**
    ```prompt
    [chorus]Maatsoort 3/4 (Walsritme)
    ```

*   **Gefluisterde tekst:**
    ```prompt
    (fluisterend) Een geheim voor jou
    ```

*   **Achtergrondkoor:**
    ```prompt
    (Achtergrondkoor: Ahhh)
    ```

*   **Dubbele nadruk:**
    ```prompt
    [chorus][[EPIC]] (Zing met maximale energie)
    ```




### Het "Perfect Prompt" (circa 300 tekens)

Dit voorbeeld combineert diverse elementen voor een optimale Suno.ai generatie:

```prompt
[intro][Nederpop-ballad, dromerig][language:Dutch] BPM 85 AABB
(Zachte piano akkoorden)

[verse]
(Zing met melancholie) De regen tikt zacht op het raam,
Een stille avond, ik fluister je naam.

[chorus][[EMOTIONEEL]][krachtige stem]
(Zing met passie) Oh, mijn liefde, waar ben je nu?
Elke ster aan de hemel herinnert me aan jou.
```



## 5. Veelgemaakte fouten & fixes

Bij het prompten in Suno.ai kunnen er enkele veelvoorkomende fouten optreden. Hieronder vind je de problemen en de bijbehorende oplossingen.

*   **Te lange prompts → Suno knipt secties af.**
    *   **Probleem:** Suno.ai heeft een limiet op de promptlengte. Te veel tekst kan leiden tot afgeknotte nummers of genegeerde instructies.
    *   **Oplossing:** Houd je prompts beknopt en to the point. Focus op de essentie van elke sectie. Gebruik sectietags om de structuur duidelijk te maken in plaats van lange beschrijvingen.

*   **Verkeerde bracketvolgorde → tags genegeerd.**
    *   **Probleem:** Incorrect geplaatste haakjes of een verkeerde volgorde kunnen ervoor zorgen dat Suno.ai je instructies negeert.
    *   **Oplossing:** Zorg ervoor dat vierkante haken `[]` worden gebruikt voor muzikale instructies en ronde haken `()` voor gezongen tekst of vocale aanwijzingen. Plaats muzikale instructies bij voorkeur aan het begin van een sectie.

*   **Té veel styles → genre clash.**
    *   **Probleem:** Het combineren van te veel uiteenlopende stijlen kan resulteren in een onsamenhangend nummer dat geen duidelijk genre heeft.
    *   **Oplossing:** Beperk het aantal stijlen per nummer tot 2-3 hoofdgenres en eventueel enkele substijlen die goed bij elkaar passen. Experimenteer met combinaties om te zien wat werkt.

*   **Onbedoeld Engels → expliciet `[language:Dutch]`.**
    *   **Probleem:** Suno.ai kan soms geneigd zijn om Engelse teksten te genereren, zelfs als je Nederlandstalige tekst invoert, vooral als de stijl of context dit suggereert.
    *   **Oplossing:** Voeg expliciet `[language:Dutch]` toe aan je prompt, bij voorkeur aan het begin van de prompt of bij elke sectie waar je Nederlandse tekst verwacht. Dit dwingt Suno.ai om de Nederlandse taal te prioriteren.

*   **Solution-snippets voor elk probleem.**
    *   **Voorbeeld te lange prompt:**
        ```prompt
        [verse][pop] (Zing over de liefde) De zon schijnt fel vandaag, mijn hart is blij.
        ```
        *Fix:* Kort en krachtig, met duidelijke sectie en stijl.

    *   **Voorbeeld verkeerde bracketvolgorde:**
        ```prompt
        (Zing over de liefde)[pop] De zon schijnt fel vandaag, mijn hart is blij.
        ```
        *Fix:* Plaats stijl-tags eerst.
        ```prompt
        [pop](Zing over de liefde) De zon schijnt fel vandaag, mijn hart is blij.
        ```

    *   **Voorbeeld te veel styles:**
        ```prompt
        [intro][rock, klassiek, hip-hop, jazz] (Chaotische start)
        ```
        *Fix:* Kies complementaire stijlen.
        ```prompt
        [intro][rock, blues] (Gitaarriff begint)
        ```

    *   **Voorbeeld onbedoeld Engels:**
        ```prompt
        [verse] (I walk alone) Ik loop alleen door de stad.
        ```
        *Fix:* Voeg taal-tag toe.
        ```prompt
        [verse][language:Dutch] (Ik loop alleen) Ik loop alleen door de stad.
        ```



## 6. Geavanceerde control-hacks

Voor de ervaren gebruiker zijn er geavanceerde technieken om nog meer controle uit te oefenen over de gegenereerde muziek.

*   **Emphasis vs. downtone:**
    *   Gebruik hoofdletters binnen vierkante haken voor extra nadruk: `[POWER CHORUS]`. Suno.ai zal proberen dit muzikaal te vertalen naar een intensere uitvoering.
    *   Gebruik ronde haken met beschrijvende termen voor een ingetogen effect: `(fluisterend couplet)`. Dit stuurt de vocale stijl.

*   **Layering vocals met dubbele haakjes:**
    *   Hoewel Suno.ai niet expliciet dubbele haakjes `((...))` ondersteunt voor layering, kun je dit simuleren door meerdere vocale instructies in ronde haakjes te plaatsen, eventueel met een korte beschrijving van de gewenste laag:
        ```prompt
        (hoofd zang) Ik zing dit lied
        (achtergrondkoor) Ooh-ooh
        (harmonieën) Mooie klanken
        ```

*   **Her-roll met identieke seed + kleine style-tweaks voor variaties:**
    *   Als je een nummer genereert, krijg je een `seed` nummer. Door dezelfde `seed` te gebruiken en slechts kleine aanpassingen te doen aan de styles of prompt, kun je variaties op hetzelfde nummer krijgen zonder volledig opnieuw te beginnen. Dit is ideaal voor het finetunen van een specifieke sfeer of instrumentatie.

*   **Prompt-chaining voor langere nummers (>2 min):**
    *   Suno.ai genereert nummers van beperkte lengte. Voor langere nummers kun je *prompt-chaining* gebruiken. Genereer het eerste deel van je nummer, kopieer de laatste paar regels en de muzikale context, en gebruik dit als startpunt voor de volgende generatie. Herhaal dit proces om een langer nummer te creëren. Let op de consistentie in stijl en tempo.



## 7. Snelkoppelingen & Cheatsheets

Om je workflow te versnellen en consistentie te waarborgen, kun je gebruikmaken van de volgende snelkoppelingen en cheatsheets.

### Stijl-shortcodes

Creëer je eigen shortcodes voor veelgebruikte stijlen om tijd te besparen en consistentie te garanderen. Dit zijn voorbeelden; je kunt ze aanpassen aan je eigen behoeften.

| Shortcode    | Volledige stijlomschrijving                               |
| :----------- | :------------------------------------------------------- |
| `NL-EDM`     | `[elektronisch, dance, upbeat, synthwave]`               |
| `Nederpop-ballad` | `[pop, ballad, melancholisch, akoestisch, nederpop]`     |
| `Trap-NL`    | `[hip-hop, trap, harde beat, Nederlandse rap]`           |
| `Rock-klassiek` | `[rock, klassiek, orkestraal, episch]`                   |
| `Jazz-smooth` | `[jazz, smooth, lounge, relaxte sfeer]`                  |

### Rijmschema-codes

Geef Suno.ai een hint over het gewenste rijmschema door de codes toe te voegen aan je prompt. Dit helpt bij het genereren van coherente teksten.

*   `AABB`: De eerste twee regels rijmen, de volgende twee ook (couplet 1: A, A, B, B; couplet 2: C, C, D, D).
*   `ABAB`: Om de andere regel rijmt (couplet 1: A, B, A, B; couplet 2: C, D, C, D).
*   `AAAA`: Alle regels rijmen (monorijm).
*   `ABCB`: De tweede en vierde regel rijmen.

```prompt
[verse][language:Dutch] AABB
Ik loop door de stad, de zon schijnt zo fel,
Geen wolkje aan de lucht, alles is wel.
De vogels zingen vrolijk hun lied,
Een mooier moment, dat bestaat niet.
```

### Lettergreep-tel-truc

Gebruik het teken `‐` (koppelteken) in je prompts om Suno.ai te helpen met de klemtoon en het ritme van de zang. Dit is vooral handig voor Nederlandse teksten waar klemtoon de betekenis kan beïnvloeden.

*   **Voorbeeld:** `(Zing met nadruk) Ik‐ ben‐ hier‐ nu!`
    *   Dit geeft aan dat elke lettergreep afzonderlijk en met nadruk gezongen moet worden.

*   **Voorbeeld:** `(Zing vloeiend) Ik ben hier nu`
    *   Zonder koppeltekens zal Suno.ai proberen de tekst vloeiender te zingen.



## 8. Best practice checklist (10 punten)

Voordat je op **Generate** klikt, doorloop deze checklist om de kwaliteit van je prompt te maximaliseren:

1.  **Duidelijke intentie:** Is het duidelijk welk genre, sfeer en structuur je wilt bereiken?
2.  **Taal gespecificeerd:** Heb je `[language:Dutch]` toegevoegd voor Nederlandstalige nummers?
3.  **Sectietags aanwezig:** Zijn alle secties (intro, verse, chorus, etc.) correct gelabeld?
4.  **Haakjes correct gebruikt:** Zijn vierkante haken `[]` voor instructies en ronde haken `()` voor gezongen tekst?
5.  **Styles relevant:** Zijn de gekozen styles passend en niet conflicterend?
6.  **BPM/Toonsoort/Maatsoort:** Indien gewenst, zijn deze muzikale parameters correct ingesteld?
7.  **Instrumentatie gespecificeerd:** Heb je de gewenste instrumenten benoemd?
8.  **Vocale descriptors:** Zijn de zangstijl en kenmerken duidelijk omschreven?
9.  **Geen overbodige tekst:** Is de prompt beknopt en vrij van onnodige informatie?
10. **Rijmschema overwogen:** Heb je een rijmschema toegevoegd als dat belangrijk is voor de tekst?



