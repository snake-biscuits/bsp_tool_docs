// TODO: links
#let zone_button(colour, title) = block[
  #set text(14pt, white)
  #box(rect(
    width: 100%,
    height: 15%,
    inset: 2em,
    fill: colour,
    align(horizon + center, strong(title))))
]


#show heading: set align(center)
#set text(font: "Noto Sans")
#set page(flipped: true)
// TODO: html export, no pages

= #raw("bsp_tool") docs

#grid(
  columns: (1fr, 1fr, 1fr, 1fr),
  rows: (auto),
  gutter: .5em,
  zone_button(rgb("#8DA"), "History"),
  zone_button(rgb("#BAE"), "Community"),
  zone_button(rgb("#DC8"), "Tools"),
  zone_button(rgb("#8AE"), "Guides"),
)


== Branches

// TODO: MediaWiki style category box
#block(fill: rgb("#EEE"), inset: .75em)[
#align(center)[
#columns(3)[
== GoldSrc
=== gearbox
blue_shift
nightfire
=== valve
goldsrc

== Source
=== ace_team
zeno_clash
=== arkane
dark_messiah_mp
dark_messiah_sp
=== loiste
infra
=== nexon
cso2
cso2_2018
vindictus
vindictus69
=== outerlight
outerlight
=== strata
strata
=== troika
vampire
=== utoplanet
merubasu
=== valve
alien_swarm
left4dead
left4dead2
orange_box
orange_box_x360
sdk_2013
sdk_2013_x360
source
source_filmmaker

#colbreak()

== Quake
=== id_software
quake
quake64
=== raven
hexen2

== ReMakeQuake
=== id_software
remake_quake
remake_quake_old

== Quake 2
=== id_software
quake2
qbism
=== ion_storm
daikatana

== Id Tech 2
=== ritual
sin

== Id Tech 3
=== id_software
qfusion
quake3
=== raven
soldier_of_fortune
soldier_of_fortune2
=== ritual
fakk2
mohaa
mohaa_bt
mohaa_demo
star_trek_elite_force2
star_trek_elite_force2_demo

#colbreak()

== IW 1.0
=== infinity_ward
call_of_duty1
call_of_duty1_demo

== IW 2.0
=== infinity_ward
call_of_duty2

== IW 3.0
=== infinity_ward
modern_warfare

== Titanfall
=== respawn
apex_legends
apex_legends50
apex_legends51
apex_legends52
titanfall
titanfall2
titanfall_x360

== Genesis3D
=== wild_tangent
genesis3d
]
]
]
