@chapter 8 | Electricity and Conductivity

@intro
Electricity questions are practical: **units of electricity** (kWh) and bill calculations, **bulb brightness and resistance**, series vs parallel, the **dynamo, motor and transformer**, **fuse, earthing and the three-pin plug**, **fluorescent tubes and CFLs**, and **solar (photovoltaic) cells**. The conductivity part covers the best conductors, **lightning conductors**, **superconductors** and **semiconductors** (silicon, germanium). It contains **{pyqs} PYQs and {ones} one-liners**.
@end

@section 8.1 | Electrical Energy and the Unit

@src 9:1
@pyq U.P.P.C.S. (Pre) 2006
The value of 1 kilowatt hour is
(a) 3.6 × 10^{6} J
(b) 3.6 × 10^{3} J
(c) 10^{3} J
(d) 10^{5} J
@ans (a)
@end

@src 9:2
@pyq U.P. Lower Sub. (Pre) 2009
An electric bulb of 100 watt is used for 4 hours. The unit of electric energy used is
(a) 400
(b) 25
(c) 4
(d) 0.4
@ans (d)
@end

@q 9:3-4

One **"unit"** on an electricity bill is **1 kilowatt-hour** = 1,000 W × 3,600 s = **3.6 × 10^{6} J**. Units = (watts × number of appliances × hours) / 1,000. So 100 W × 4 h = 0.4 unit; 5 × 100 W × 20 h = 10 units; 15 × 200 W × 24 h = **72 units**. (The 2023 question used the **Silkyara tunnel**, Uttarakhand, where 41 workers were rescued in November 2023.)

@section 8.2 | Resistance, Bulbs and Circuits

@q 9:5

Power **P = V^{2}/R** at a fixed household voltage (230 V in India), so the bulb with **less resistance draws more power and glows brighter**; the dim bulb has the larger resistance. A 100 W bulb has less resistance than a 40 W bulb.

@q 9:6

In **parallel**, each bulb gets the full mains voltage and glows at full power; in **series** they share the voltage, and two identical bulbs give only a quarter of the total light. Houses are therefore wired in parallel, so each appliance works independently.

@q 9:7

**Ohm's law: V = IR.** Resistor colour code: brown = 1, green = 5, black = multiplier 10^{0}, so R = 15 Ω and I = 15 V / 15 Ω = **1 A**. (Code order: black 0, brown 1, red 2, orange 3, yellow 4, green 5, blue 6, violet 7, grey 8, white 9.)

@q 9:15

@src 9:24
@pyq U.P. Lower Sub. (Mains) 2015
Small drops of the same size are charged to V volts each. If n such drops coalesce to form a single large drop, its potential will be :
(a) n^{2/3} V
(b) n^{1/3} V
(c) n V
(d) n^{-1} V
@ans (a)
@end

Charge adds up (Q = nq) but the radius grows only as n^{1/3} (volume is conserved), and potential = kQ/R, so the big drop's potential is **n^{2/3} V**.

@section 8.3 | Dynamo, Motor and Transformer

@q 9:8-11

@qnote 9:9 | The source gives **(c) & (d)**. The **dynamo** (generator) is the classic electromagnetic-induction device, turning mechanical energy into electrical. A **motor** works on the force on a current-carrying conductor in a magnetic field, though induction (back e.m.f.) also acts inside it, and induction motors are named after it.

@table
Device | Principle / job
**Dynamo (generator)** | Electromagnetic induction (Faraday): mechanical → electrical
**Electric motor** | Force on a current in a magnetic field: electrical → mechanical
**Transformer** | Mutual induction: steps **AC** voltage up or down (does not work on DC)
**Rectifier** (diode) | **AC → DC**
**Inverter** | **DC → AC** (home inverters, solar inverters)
UPS | Battery backup that switches instantly
Mobile charger | **Step-down transformer** (or switch-mode circuit) plus rectifier
@end

A motor draws power P = VI; at **low voltage** it draws **more current** to keep turning its load, and the extra current overheats and burns its windings. That is why voltage stabilisers are used with ACs and refrigerators.

@q 9:25-26

@src 9:27
@pyq U.P.P.C.S. (Pre) 2006
The device used for converting alternating current to direct current is called
(a) Inverter
(b) Rectifier
(c) Transformer
(d) Transmitter
@ans (b)
@end

Power is transmitted at **very high voltage** (up to 765 kV AC and 800 kV HVDC in India) because for the same power, higher voltage means lower current and much lower I^{2}R loss in the lines; transformers then step it down for homes.

@section 8.4 | Safety: Fuse, Earthing and Plugs

@q 9:12-14

The **earth pin** is the **longest and thickest** pin of a three-pin plug: it connects first and disconnects last, so the metal body of an appliance is always grounded and a leak of current flows to earth instead of through a person. **Live** wire is red or brown, **neutral** black or blue, and **earth** green or green-yellow.

@q 9:16-17

A **fuse** wire must melt quickly when current is too high, so it has **high resistance and a low melting point**. The usual material is a **lead-tin alloy** (about 200°C melting point), far below copper (1,085°C) and aluminium (660°C), so the Reason in the 2025 question is false. Homes now mostly use **MCBs** (miniature circuit breakers), which trip and can be reset.

@section 8.5 | Lamps and Lighting

@q 9:18-20

@q 9:21-23

@qnote 9:21 | The source gives **(b) & (c)**: a tube light holds **mercury vapour** and an inert gas (usually **argon**), both at low pressure.

@table
Lamp | How it works | Efficiency
**Incandescent bulb** | **Tungsten** filament heated white-hot (melting point 3,422°C) in inert gas (argon, nitrogen) | About 5% of energy becomes light
**Fluorescent tube / CFL** | Discharge in **mercury vapour + argon** gives UV; the **phosphor** coating turns it into visible light | 4-5 times better than a bulb
**LED** | Semiconductor diode emits light directly | Best; 10 times a bulb, very long life (**UJALA** scheme, 2015)
**Neon sign** | Discharge in **neon** gives orange-red; other gases give other colours | Advertising
**Sodium vapour lamp** | Yellow light | Street lights
@end

@section 8.6 | Solar Cells and the Earth's Magnetism

@q 9:28

Order of power: **fan (about 75 W) < television (100-150 W) < electric iron (750-1,000 W) < electric kettle (1,500-2,000 W)**. Heating appliances use the most power.

@q 9:29-30

A **photovoltaic (solar) cell** converts sunlight directly into electricity using a semiconductor (usually **silicon**) p-n junction. A **Leclanché cell** and a **dry cell** are chemical cells; a voltaic cell is the first chemical battery (Volta, 1800).

@q 9:31

The Earth's magnetic field comes from **electric currents in the molten iron outer core** (the *geodynamo*), not from a giant bar magnet. The field has reversed many times in geological history.

@section 8.7 | Conductors and Lightning

@q 10:1

Best conductors in order: **silver > copper > gold > aluminium**. Copper is used for wiring because it is nearly as good as silver and far cheaper; aluminium is used in overhead lines because it is light. **Mica** is an insulator.

@q 10:2-4

A **lightning conductor** is a pointed metal rod (usually **copper**, which conducts well and does not rust) on top of a building, joined by a thick strip to a plate buried in the ground; it leads the charge safely to earth. A **closed car** (metal body) acts as a **Faraday cage**: the charge stays on the outside surface and the people inside are safe. During a storm, avoid open fields, lone trees and water; crouch low. **Damini** is the lightning-warning app of the Ministry of Earth Sciences.

@section 8.8 | Superconductors and Semiconductors

@q 10:5

@src 10:6
@pyq U.P. Lower Sub. (Pre) 2013
The highest temperature attained by a superconductor is :
(a) 24 K
(b) 133 K
(c) 150 K
(d) 300 K
@ans (*)
@note When the question was set, the record was **about 133-138 K** (mercury-based cuprate ceramics), so (b) was the intended answer. Later claims of near-room-temperature superconductivity at extreme pressures (hydrides, 2015-2020) and the **LK-99** claim (2023) were not confirmed at normal pressure, so the source marks the question (*).
@end

@src 10:7
@pyq U.P.P.C.S. (Pre) 2000
The newly discovered high temperature super conductors are
(a) Metal alloys
(b) Pure rare earth metals
(c) Ceramic oxides
(d) Inorganic polymers
@ans (c)
@end

A **superconductor** has **zero resistance** below a critical temperature and expels magnetic fields (Meissner effect). It was discovered in mercury at 4.2 K (Kamerlingh Onnes, 1911). **High-temperature** superconductors (1986 onwards) are **copper-oxide ceramics** that work above 77 K, the boiling point of liquid nitrogen. A **room-temperature** superconductor would save the huge losses in power transmission. Uses: MRI magnets, **maglev** trains, particle accelerators, fusion reactors.

@q 10:8-12

@table
Material | Resistance on heating | Examples
**Conductor** | Increases | Metals (silver, copper, aluminium)
**Semiconductor** | **Decreases** (more charge carriers freed) | **Silicon**, **germanium**, gallium arsenide
**Insulator** | Very high always | Glass, mica, rubber, plastic, wood, quartz, ceramics
@end

Adding small impurities (**doping**) controls a semiconductor: phosphorus or arsenic gives **n-type**, boron or gallium **p-type**. **Silicon** (from sand) is the base of almost all chips; India's **Semicon India** programme (2021) backs fabs and assembly plants, the first being Tata's fab at **Dholera** (Gujarat) and Micron's assembly unit at **Sanand**.

@trap
**1 unit = 1 kWh = 3.6 × 10^{6} J.** The **dimmer bulb has higher resistance**. Bulbs in **parallel** glow brighter. A **dynamo** works on electromagnetic induction; a **transformer works only on AC**; a **rectifier** turns AC to DC. A **fuse** has **high resistance and low melting point** (lead-tin). The earth pin is **longest and thickest**. **Silver** is the best conductor. A semiconductor's resistance **falls** on heating.
@end

@heatmap

@pattern
Electricity questions are **numerical and practical**: bills in units, bulb brightness, the colour code. Recent papers (2021-2025) put these numbers in news contexts (the Silkyara tunnel), and the 2025 paper turned the fuse wire into Assertion-Reason. Semiconductors and superconductors are steady conceptual favourites.
@end

@next
Likely next angles: **Semicon India** fabs and the **India Semiconductor Mission**, **LED** savings under UJALA, **smart meters** and **prepaid meters**, **HVDC** lines (Raigarh-Pugalur), **lithium-ion** vs **sodium-ion** batteries, **EV** charging, **graphene**, the **PM Surya Ghar** rooftop solar scheme (2024), and **perovskite** solar cells.
@end
