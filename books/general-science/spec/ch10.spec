@chapter 10 | Computer and Information Technology
@unit UNIT II · SCIENCE AND TECHNOLOGY

@intro
The computer questions test **basic literacy**: full forms (WWW, RAM, ROM, SIM, UPS, ICT, ATM), units of memory (**bit, byte, KB, GB**), hardware (CPU, input and output devices, printers, ICs made of silicon, generations of computers), software (operating systems, languages, assembler), networks (internet, protocols, modem, OSI layers, Wi-Fi and **Li-Fi**), **Indian supercomputers** (PARAM, Anupam) and threats (virus, bug, **Stuxnet**). It contains **{pyqs} PYQs and {ones} one-liners**.
@end

@section 10.1 | History and Supercomputers

@q 12:1-2

**Charles Babbage** (1791-1871) designed the Difference Engine and the **Analytical Engine** (1837), the first plan for a general-purpose computer, and is called the **father of the computer**; **Ada Lovelace** wrote the first program for it. The first electronic general-purpose computer was **ENIAC** (1946). **Douglas Engelbart**'s first mouse (1964) had a **wooden** shell.

@q 12:47-48

@table
Generation | Period | Main component
First | 1940-56 | **Vacuum tubes** (ENIAC, UNIVAC)
Second | 1956-63 | **Transistors**
Third | 1964-71 | **Integrated circuits (ICs)**
Fourth | 1971-present | **Microprocessors** (VLSI)
Fifth | Present and future | **Artificial intelligence**, parallel processing, quantum computing
@end

@q 12:49-51

An **integrated circuit** (Jack Kilby, 1958) packs many transistors on one **silicon** chip; ICs are graded by the number of transistors: SSI, MSI, LSI, **VLSI**, ULSI. Silicon is cheap, abundant (from sand) and a good semiconductor; gallium arsenide is used for faster or optical chips.

@q 12:11-13

@src 12:14
@pyq U.P. Lower Sub. (Pre) 1998
The world's fastest computer has been able to perform (as of Dec. 1996) :
(a) 10^{6} operations per second
(b) 10^{9} operations per second
(c) 10^{12} operations per second
(d) 10^{15} operations per second
@ans (c)
@end

@pyq U.P. Lower Sub. (Pre) 2008
The fastest computer in the world is –
(a) Param-10000
(b) J-8
(c) Yenha-3
(d) T-3A
@ans (*)
@note None of the options was the world's fastest machine at the time (China's **Tianhe-1A** led the TOP500 in 2010), so the source marks the question (*). The fastest today is **El Capitan** (USA, about 1.7 exaflops, from November 2024).
@end
@src 12:15

@q 12:16

@table
Supercomputer | Developer | Note
**PARAM 8000** (1991) | **C-DAC, Pune** | India's first indigenous supercomputer; PARAM 10000 (1998), PARAM Padma, PARAM Siddhi-AI, PARAM Rudra (2024)
**Anupam** | **BARC** | Parallel supercomputers for nuclear research
**Flosolver** | NAL, Bengaluru | Aerodynamics
**Pratyush** and **Mihir** | IITM Pune / NCMRWF Noida | Weather and climate (2018)
**AIRAWAT** | C-DAC | AI supercomputer under the National Supercomputing Mission
**Arka** and **Arunika** (2024) | IITM / NCMRWF | New weather supercomputers
@end

The **teraflop** (10^{12} operations per second) mark was first passed by **ASCI Red** (Intel, USA) in December 1996. India's **National Supercomputing Mission** (2015) builds PARAM systems across institutes. **Magic Cube** (Dawning 5000A, 2008) was Chinese.

@q 12:18

A **quantum computer** uses **qubits**, which can be 0 and 1 at once (superposition), and can be vastly faster for certain problems. India's **National Quantum Mission** (2023) aims at 50-1,000 qubit machines by 2031.

@q 12:17

@section 10.2 | Hardware and Memory

@q 12:42-46

@src1 12:4

@table
Input devices | Output devices | Both
**Keyboard, mouse, scanner**, joystick, light pen, microphone, webcam, barcode reader, OCR, MICR (cheques) | **Monitor, printer, projector**, speaker, plotter | Touchscreen, modem, network card
@end

@one
Which of the following statements is correct?
@ans CPU refers to Central Processing Unit
@end

The **CPU** (the "brain") has the **ALU** (arithmetic and logic), the **control unit** and registers. Intel Core i3/i5/i7/i9 and AMD Ryzen are **processors**.

@q 12:30-32

@src1 12:3
@one
Which of the following relation is correct?
@ans 1 Gigabyte = 1024 Megabytes
@end

@one
In the binary system, one kilobyte (KB) is equal to
@ans 1024 bytes
@end

@q 12:33-35

@table
Unit | Size
**Bit** (binary digit) | 0 or 1, the smallest unit
Nibble | 4 bits
**Byte** | **8 bits** (one character)
Kilobyte (KB) | 1,024 bytes
Megabyte (MB) | 1,024 KB
Gigabyte (GB) | 1,024 MB
Terabyte (TB) | 1,024 GB
Petabyte, exabyte, zettabyte | Each 1,024 times the one before
@end

A **MAC address** is a 48-bit (6-byte) hardware address fixed in a network card; an IPv4 address is 32 bits and IPv6 is 128 bits. **5211, 2421 and 3321** are *self-complementing* codes (the 9's complement of a digit is got by inverting its bits).

@q 12:53-57

@table
Memory | Nature
**RAM** (Random Access Memory) | Working memory; **volatile** (lost when power goes off)
**ROM** (Read Only Memory) | **Non-volatile**, permanent; holds the start-up (BIOS) program
**Cache** | Very small, **fastest**, between CPU and RAM
Registers | Inside the CPU, faster still
Hard disk, SSD | Secondary, permanent storage
**Flash memory** | Non-volatile chip memory (pen drives, SSDs, cameras); faster and tougher, but costlier per GB than a hard disk
@end

@src 12:36
@pyq U.P.P.C.S. (Pre) 1999
Computer hardware, which can store a very large quantity of data, is called :
(a) Magnetic tape
(b) Disk
(c) Both (a) and (b)
(d) None of the above
@ans (c)
@end

@q 12:37-39

@q 12:19-20

**Laser printers** use a **semiconductor laser** to draw the page on a drum; **inkjet** printers spray ink; **dot-matrix, daisy-wheel and line** printers strike a ribbon and are **impact** printers. The keyboard used to plug into a PS/2 port; today it uses **USB**.

@section 10.3 | Software and Languages

@q 12:40-41

The **operating system** (Windows, Linux, Unix, macOS, Android, iOS; India's **Maya OS** for defence, **BharOS** for phones) manages hardware and runs programs. **MS Office** is application software. **Multitasking** is running several applications at once.

@q 12:63

@q 12:58

@src 12:59
@pyq U.P. Lower Sub. (Mains) 2013
BASIC is a ......language ?
(a) A procedural
(b) An object oriented
(c) Both (a) and (b)
(d) None of the above
@ans (a)
@end

@q 12:60

@table
Language / tool | Use
**FORTRAN** (1957, IBM) | Formula Translation: **scientific** computing
**COBOL** | Business data processing
**BASIC** | Beginners' **procedural** language
**C** (Dennis Ritchie) | Systems programming, operating systems
C++, **Java**, Python | **Object-oriented** programming
**Assembler** | Assembly language → machine language
**Compiler** | Whole high-level program → machine language at once
**Interpreter** | High-level program → machine language line by line
@end

@q 12:27-29

A **virus** is a malicious program that copies itself into other files; a **worm** spreads by itself across networks; a **trojan** hides inside useful-looking software; **ransomware** locks data for payment. **Stuxnet** (found 2010) was a worm that damaged Iran's uranium-enrichment **centrifuges** at Natanz, the first known cyber-weapon. A **bug** is an error in a program. **CERT-In** is India's national cyber-security agency.

@q 12:9-10

@section 10.4 | Internet and Networks

@q 12:5-6

@pyq U.P. Lower Sub. (Mains) 2015
The internet works on :
(a) Circuit switching only
(b) Packet switching only
(c) Both circuit and packet switching
(d) None of the above
@ans (b)
@end
@src 12:7

@pyq U.P. Lower Sub. (Mains) 2013
The layer between Physical and Network layer is known as?
(a) Data Link Layer
(b) Transport Layer
(c) Session Layer
(d) None of the above
@ans (a)
@end
@src 12:8

The internet breaks data into **packets** that travel by different routes and are rejoined (**packet switching**); the old telephone network kept a dedicated line open (**circuit switching**). The **OSI model** has seven layers, bottom to top: **Physical, Data Link, Network, Transport, Session, Presentation, Application** ("Please Do Not Throw Sausage Pizza Away").

@q 12:26

@q 12:23-25

@q 12:61

@src 12:21
@pyq U.P.P.C.S. (Mains) 2010; U.P.P.C.S. (Pre) 2015
The full form of www is –
(a) Web Working Window
(b) World Working Web
(c) World Wide Web
(d) Window World Wide
@ans (c)
@note The source prints the key as (d), an obvious misprint: WWW stands for **World Wide Web**, option (c).
@end

@src1 12:2
@one
Who is considered the inventor of the World Wide Web (www)?
@ans Tim Berners-Lee
@end

**Tim Berners-Lee** created the Web at **CERN** in 1989-91: web pages (HTML) linked by hyperlinks and fetched with **HTTP**. The internet itself grew from the US **ARPANET** (1969). A **protocol** is a set of rules for data communication (TCP/IP, HTTP, FTP, SMTP). **Archie** was the first internet search tool, and **Finger** looked up a user's details.

@q 12:52

@src1 12:5
@src1 12:6
@one
Which of the following is necessary for exchanging data among computers all over the world through telephone lines?
@ans Modem
@end

@one
Which system or arrangement connects a microcomputer to a telephone?
@ans Modem
@end

A **modem** (*modulator-demodulator*) converts a computer's digital signals into analogue signals for a telephone line and back.

@q 12:22

@pyq U.P. Lower Sub. (Mains) 2015
The first railway station in the country to provide Google's free public Wi-Fi service is :
(a) New Delhi Railway Station
(b) Mumbai Central Railway Station
(c) Howrah Railway Station
(d) Chennai Railway Station
@ans (b)
@end
@src 12:3

@pyq U.P. R.O./A.R.O. (Pre) 2017
Which one of the following statements is not true about Li-Fi?
(a) The full form of Li-Fi is 'Light Fidelity'
(b) The successful test of Li-Fi in India was done by Ministry of Information and Broadcasting on 29th January, 2018
(c) Li-Fi can send 10 GB/sec. data up to 1 km circumference
(d) It is operated by optical fibre network
@ans (b) & (d)
@note The source gives **(b) & (d)**. Li-Fi sends data through flickering **LED light**, not optical fibre, and India's first successful trial (January 2018) was by the **Ministry of Electronics and IT** with IIT Madras, not the I&B Ministry.
@end
@src 12:4

**Bluetooth** is short-range wireless (radio, 2.4 GHz) between devices; **Wi-Fi** is wireless local networking by radio; **Li-Fi** (Harald Haas, 2011) uses **visible light**. Google and RailTel's free station Wi-Fi began at **Mumbai Central** in January 2016.

@q 12:64

@q 12:68

@section 10.5 | Full Forms and IT in Governance

@q 12:65-67

@src 12:69
@pyq U.P. Lower Sub. (Pre) 2015
The full form of UPS is
(a) Uninterrupted Power Supply
(b) Universal Power Supply
(c) Universal Power Service
(d) Universal Power Saving
@ans (a)
@end

@table
Short form | Full form
**WWW** | World Wide Web
**HTTP / HTTPS** | HyperText Transfer Protocol (Secure)
**URL** | Uniform Resource Locator
**RAM / ROM** | Random Access Memory / Read Only Memory
**CPU / ALU** | Central Processing Unit / Arithmetic Logic Unit
**SIM** | Subscriber Identity Module
**UPS** | Uninterruptible Power Supply
**ICT** | Information and Communication Technology
**ATM** | Automated Teller Machine
**OCR** | Optical Character Recognition
**Modem** | Modulator-Demodulator
**PDF** | Portable Document Format
@end

@q 12:62

@q 12:70-72

E-governance makes government **cheaper, faster and more transparent** and lets citizens give more input; it reduces, not increases, red tape. Indian examples: **DigiLocker, UMANG, e-District, CoWIN, GeM**, the **Digital India** programme (2015) and **UPI**. **Vidya Vahini** (2002) was a scheme to give schools computers and connectivity.

@up UP link: UP uses **e-District** for certificates, **IGRS (Jansunwai)** for grievances, and **Nivesh Mitra** for business approvals; **Noida** is the state's IT and electronics hub, with a large share of India's mobile-phone manufacturing.

@trap
**Charles Babbage** = father of the computer. **IC = third generation**, microprocessor = fourth. **1 byte = 8 bits**; 1 KB = **1,024** bytes. **RAM is volatile**, ROM is not; **cache** is fastest. **Microsoft Office is not an operating system.** **FORTRAN = scientific**, BASIC = procedural. An **assembler** converts assembly to machine code. Internet = **packet switching**. **Li-Fi uses light**, not fibre. **Stuxnet** attacked Iranian centrifuges.
@end

@heatmap

@pattern
Computer questions are the most numerous single block in General Science, driven by the **Lower Subordinate (Mains)** papers of 2013 and 2015, which asked basic terminology in bulk. The Prelims now ask one or two (2023-2024: MAC address, i9 processor, ROM, input devices, e-governance), mostly at a beginner level.
@end

@next
Likely next angles: **AI** terms (LLM, generative AI, the **IndiaAI Mission** and its GPU compute), **quantum computing** (National Quantum Mission), **semiconductor fabs** (Dholera), **5G/6G**, **cyber-security** (CERT-In, ransomware, deepfakes, the **DPDP Act 2023**), **UPI** and digital public infrastructure, **blockchain**, and **cloud** services.
@end
