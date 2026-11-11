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
#block(fill: rgb("#DDD"), inset: .75em)[
#columns(3)[
  == idTech

  === Quake
  - hexen2
  - quake
  - remake_quake

  === Quake 2
  - daikatana
  - qbism
  - quake2

  === Quake 3
  - fakk2
  - mohaa
  - mohaa_bt
  - mohaa_demo
  - qfusion
  - quake3
  - star_trek_elite_force2
  - star_trek_elite_force2_demo

  #colbreak()

  == IW

  === 1.0
  - call_of_duty_demo
  - call_of_duty

  === 2.0
  - call_of_duty2

  === 3.0
  - modern_warfare

  == ReSource

  === Titanfall
  - titanfall
  - titanfall_x360

  === Titanfall 2
  - titanfall2

  === Apex Legends
  - apex_legends
  - apex_legends50
  - apex_legends51
  - apex_legends52

  #colbreak()

  == Valve

  === GoldSrc
  - goldsrc
  - blue_shift

  === Source
  - orange_box
  - orange_box_x360
  - sdk_2013
  - sdk_2013_x360
  - source
  - source_xbox

  == Other
  === Arkane
  - dark_messiah_mp
  - dark_messiah_sp

  === Strata
  - strata

  === Troika
  - vampire

  === Utoplanet
  - merubasu
]
]
