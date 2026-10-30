@chapter 3 | Mechanics and Motion under Gravity

@intro
Mechanics questions test everyday applications of **Newton's laws**: inertia in a moving bus, friction on ice, scalars and vectors, average speed, kinetic energy and energy conversions. The gravity half covers **weight vs mass**, the variation of **g** (poles vs equator, lifts), the **inverse-square law**, pendulum clocks, satellites, weightlessness and **escape velocity** (why the Moon has no air). It contains **{pyqs} PYQs and {ones} one-liners**.
@end

@section 3.1 | Quantities, Motion and Inertia

@q 2:1

A **scalar** has magnitude only (distance, speed, time, mass, work, energy, electric potential); a **vector** has magnitude and direction (**displacement, velocity, acceleration, force, momentum, weight**).

@q 2:2

@src 2:3
@pyq U.P.P.S.C. (Pre) 2003
What is the correct equation for finding the acceleration?
(a) a = (v - u)/t
(b) a = u + vt
(c) a = (v + u)/t
(d) a = (v + u)/2
@ans (a)
@end

From **v = u + at**, acceleration a = (v - u)/t, where u is initial velocity, v final velocity and t time. The other two equations of motion are **s = ut + ½at^{2}** and **v^{2} = u^{2} + 2as**.

@src 2:4
@pyq U.P.P.C.S. (Pre) 2024
A bus covers the first half of a certain distance with speed v_{1} and the second half with a speed v_{2}. The average speed during the whole journey is :
(a) v_{1}v_{2}/(v_{1} + v_{2})
(b) 2v_{1}v_{2}/(v_{1} + v_{2})
(c) (v_{1} + v_{2})/2
(d) √(v_{1}v_{2})
@ans (b)
@end

For **equal distances**, average speed = total distance / total time = d / (d/2v_{1} + d/2v_{2}) = **2v_{1}v_{2}/(v_{1} + v_{2})**, the *harmonic mean*. For **equal times** it would be the simple mean (v_{1} + v_{2})/2. Example: 40 km/h and 60 km/h over equal halves give 48 km/h, not 50.

@q 2:5-6

**Inertia** is a body's tendency to keep its state of rest or motion (Newton's first law). When a bus starts, the feet move with it but the upper body stays at rest, so passengers lean **backward** (*inertia of rest*); when it brakes, they lurch **forward** (*inertia of motion*). A washing-machine drier and a cream separator work by **centrifugation**.

@q 2:7-8

**Friction** opposes motion. *Static* friction (before movement starts) is greater than *kinetic* friction (once moving), so a cart is harder to start than to keep rolling. Ice offers little friction, so the foot slips. Rolling friction is the smallest, which is why wheels and ball bearings help.

@section 3.2 | Energy

@q 2:9
@qnote 2:9 | The source gives **(a) & (b)** as the answer: neither **nuclear** energy (from the atomic nucleus) nor **geothermal** energy (heat of the Earth's interior, largely from radioactive decay) comes from the Sun. Wind, biomass, fossil fuels, hydro and wave energy are all stored solar energy. **Tidal** energy comes mainly from the Moon's gravity.

@q 2:10

@src 2:11
@pyq U.P.P.C.S. (Pre) 2023
Non-conventional energy sources are those energy sources, that are
(a) Produced from heat
(b) Produced from electricity
(c) Non-renewable electricity
(d) Renewable
@ans (d)
@end

@src 2:12
@pyq U.P.P.C.S. (Mains) 2002
Match List-I with List-II and choose the correct answer from the code given below
@match
List-I (Energy Conversion) | List-II (Device/Mechanism)
A. Light to electric | 1. Car Braking
B. Electric to sound | 2. Nuclear reactor
C. Mass to heat | 3. Loudspeaker
D. Chemical to heat and light | 4. Solar cell
- | 5. Fuel combustion
@endmatch
Code : A B C D
(a) 1 2 3 4
(b) 4 3 2 5
(c) 2 1 3 5
(d) 3 1 2 4
@ans (b)
@end

@table
Device | Energy conversion
**Solar cell** | Light → electrical
**Loudspeaker** | Electrical → sound
Microphone | Sound → electrical
**Electric motor** | Electrical → mechanical
**Generator / dynamo** | Mechanical → electrical
**Battery (discharging)** | Chemical → electrical
**Nuclear reactor** | Mass → heat (E = mc^{2})
Electric bulb | Electrical → light and heat
Car braking | Kinetic → heat
@end

@src 2:13
@pyq U.P. R.O./A.R.O. (Pre) 2017
The ratio of kinetic energies of two bodies of same mass is 4 : 9, the ratio of their velocities will be
(a) 4 : 9
(b) 2 : 3
(c) 16 : 81
(d) √2 : √3
@ans (b)
@end

Kinetic energy = **½mv^{2}**. For equal masses KE ∝ v^{2}, so v_{1} : v_{2} = √4 : √9 = **2 : 3**. Doubling speed makes KE four times; that is why stopping distance rises so sharply with speed. *Momentum* p = mv, and KE = p^{2}/2m.

@section 3.3 | Gravity, Weight and Mass

@q 3:1

A body stays upright while the **vertical line through its centre of gravity falls inside its base**. The Leaning Tower of Pisa tilts by about 4° but its centre of gravity is still over the base. A low centre of gravity and a wide base give stability (racing cars, buses loaded below).

@q 3:2

Galileo showed that, without air resistance, **all bodies fall with the same acceleration g ≈ 9.8 m/s^{2}**, whatever their mass. In air, a feather falls slower only because of air resistance.

@q 3:3-4

@table
Situation | Effect on g or weight
**Poles** | g maximum (9.83 m/s^{2}): Earth is flattened and does not spin you outward there
**Equator** | g minimum (9.78 m/s^{2}): larger radius and greatest centrifugal effect
Going **up** a mountain or **down** a mine | g decreases (it is zero at the centre)
If Earth **stopped rotating** | g would increase at every place except the poles
Lift **accelerating up** | Apparent weight increases: m(g + a)
Lift **accelerating down** | Apparent weight decreases: m(g - a)
Lift falling **freely** | Weightless (apparent weight zero)
Lift at **constant velocity** | Weight unchanged
On the **Moon** | g is about 1/6 of Earth's
@end

Weight measured in a fluid is reduced by **buoyancy** (upthrust = weight of fluid displaced). Hydrogen is the least dense of the four media, so the upthrust is least and the body weighs most in it.

@q 3:5-6

The time period of a simple pendulum is **T = 2π√(l/g)**. In summer the metal rod **expands**, l increases, each swing takes longer and the clock runs **slow**; in winter it gains time. On the Moon (smaller g) a pendulum clock would also run slow, and in a freely falling lift or orbit it would stop.

@q 3:7

Newton's law of gravitation: **F = Gm_{1}m_{2}/r^{2}**. Force varies as the inverse square of distance, so doubling r makes F **one-fourth**; halving r makes it four times.

@q 3:8-9

**Mass** is the quantity of matter and stays the same everywhere; **weight** (W = mg) is the force of gravity on it and changes with g. Without gravity, weight would be zero but mass unchanged.

@section 3.4 | Satellites and Escape Velocity

@q 3:10-11

Astronauts in orbit are **weightless** not because gravity is absent (at 400 km it is still about 90% of surface gravity) but because they and their spacecraft are in **free fall** together around the Earth. An apple let go inside or beside the craft simply keeps moving with it. The source's wording "no gravity" is the exam-style explanation.

@src 3:12
@pyq U.P.P.C.S. (Pre) 2006
A Geosynchronous satellite continuously active in its orbit due to centripetal force which is obtained by
(a) The rocket engine that propelled the satellite.
(b) The gravitational force on the satellite by the earth.
(c) The gravitational force on the satellite by the sun.
(d) The gravitational force on the earth by satellite.
@ans (b)
@end

@q 3:13

The **centripetal force** that keeps a satellite circling is supplied by the **Earth's gravity**. Orbital speed near the surface is about **7.9 km/s**; a **geostationary** satellite (35,786 km up, period 24 h, over the equator) appears fixed in the sky.

@q 3:14

@table
Body | Escape velocity
**Earth** | **11.2 km/s**
Moon | 2.4 km/s
Jupiter | About 59.5 km/s
Sun | About 618 km/s
@end

Escape velocity (v_{e} = √(2gR)) does not depend on the mass of the escaping body. On the Moon it is so low that gas molecules, moving at their thermal (root mean square) speeds, escape easily, so the Moon cannot hold an atmosphere.

@trap
**Displacement, velocity, force and weight are vectors**; distance, speed, work and potential are scalars. Average speed for equal distances is **2v_{1}v_{2}/(v_{1} + v_{2})**, not the simple mean. Weight is **maximum at the poles**. Pendulum clocks **lose** time in summer. Doubling distance makes gravity **one-fourth**. Weightlessness in orbit is **free fall**, not zero gravity. **Earth's escape velocity = 11.2 km/s.**
@end

@heatmap

@pattern
These are reasoning questions dressed as everyday situations: the lift, the bus, the pendulum clock, the bucket and the astronaut. Most have been asked since the 1990s and keep returning; the **2022-2024** papers added numerical items (average speed formula, energy sources), so expect a short calculation each year.
@end

@next
Likely next angles: **Newton's third law** (rocket propulsion, recoil of a gun), **conservation of momentum**, **projectile** range at 45°, **Kepler's laws**, **Lagrange points** (Aditya-L1 at L1), the **geostationary vs polar orbit** distinction, **microgravity** experiments on the ISS (Shubhanshu Shukla's Axiom-4 mission, 2025), and **g** on the Moon and Mars.
@end
