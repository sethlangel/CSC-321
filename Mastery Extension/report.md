# CSC 321 - Spring 2025: Mastery Extension

## RFID Access Control Security: Hands On Analysis with Raspberry Pi Pico

**Seth Langel**

---

## Introduction

In an increasingly connected world, access control systems have become a cornerstone of both physical and digital security. Among these, RFID (Radio Frequency Identification) technology is one of the most commonly used methods for authenticating users. Devices such as cards have the potential to open doors to cards that authorize payment or attendance at events. With these devices a simple wave or tape is all it takes to perform these operations. But what if someone could replicate that tap without ever touching your card?

This project explores a critical question which is how secure are low cost RFID systems, particularly those using chips such as MFRC522, against spoofing attacks that replicate card UIDs? Despite their convenience, many of these systems depend solely on a card’s UID for authentication.

The goal of this research is to demonstrate the vulnerabilities of UID based RFID authentication using a hands-on security test bench built with a Raspberry Pi Pico and an MFRC522 low-frequency RFID reader. By simulating both legitimate use and spoofing attempts, this project aims to highlight how easily such systems can be bypassed and what potential countermeasures that can improve security. Ultimately, this investigation serves as a reminder that convenience should never come at the cost of security.

---

## Body

### Background and Context of RFID Systems

RFID technology enables contactless data exchange using electromagnetic fields. It’s widely used in access control systems for buildings, school IDs, payment systems, and transportation passes. Each RFID card or tag typically contains a Unique Identifier (UID), which is transmitted from the chip to the RFID reader when placed in close proximity to it. In these systems when the UID is transmitted it runs the UID against a database to see if that specific UID has credentials to perform that action.

---

### Security Concerns: The problem with UID-Based Access Control

A major vulnerability of systems that use the MFRC522 RFID reader is that the UID is not encrypted or protected in any way. The UID that is being broadcasted is done openly and can be recorded and captured by anyone that has a RFID reader in range. Once obtained, a bad actor can clone the UID using a writable RFID card.

This problem has real world implications such as budget systems that exist in schools, offices and hobby environments that use UID only checks. Unfortunately, RFID cloning tools and emulators are cheap and readily available to those who wish to impersonate valid users with very little knowledge or skill.

---

### Implementation: RFID Security Test Bench

To explore this vulnerability and demonstrate potential defenses, I developed a security test bench using a Raspberry Pi Pico microcontroller, MFRC522 LF RFID Reader, and a basic logging and LED alert system. The test bench can both read and write RFID cards, allowing me to simulate both normal use and spoofing attempts.

This testbench serves as a component in an overall RFID security system designed for controlling access to rooms or buildings. In the complete implementation, the security system would contain a servo that is connected to a deadbolt that will unlock when authentication is successful and remain locked when unsuccessful. For testing purposes this testbench will just contain the RFID security system and exclude the servo allowing it to focus primarily on the RFID security functionality.

**IMAGE OF WHOLE SYSTEM**

The RFID Security System testbench contains the following components:
- Raspberry Pi Pico Microcontroller  
- MFRC522 Low Frequency RFID Reader  
- Green LED  
- Red LED  
- Low Frequency RFID Tags  

**IMAGE OF TESTBENCH DIAGRAM**

We will be utilizing the Raspberry Pi Pico as our microcontroller to handle the logic of our testbench working hand in hand with a MFRC522 board to read, write, and spoof our RFID tags. The LEDs provide immediate visual feedback to indicate whether access is granted or denied, allowing for simple monitoring during testing. For more granular monitoring each action is logged into a text file with a timestamp, RFID chip UID and whether or not access is granted.

---

## Improving Security on a Budget

While upgrading to cryptographically secure RFID hardware is ideal, there are practical enhancements that can be implemented even with basic hardware like our testbench.

### Secure Sector Authentication

The MFRC522 can authenticate and read from protected memory sectors. With this we can write a randomly generated secure token to the card and verify that token can provide additional layers of protection.

### Analysis and Logging 

By logging and keeping track of UID scans we can see when a particular UID is being repeatedly scanned in short time spans, has suspicious patterns, or even granted access at different locations at the same time. 

### Multi Factor

Having a simple MFA system such as a PIN or button sequence in addition to the RFID card is another way to ensure basic security and reduces spoofing risks even with weak RFID authentication.  

---

## Project Results

Through testing, it became clear that relying solely on UID verification is inadequate for any use involving personal access or authentication. However, even with cheap hardware, it is possible to implement simple and practical safeguards that will decrease the chances of a successful spoofing attempt. This reinforces the idea that security conscious design is achievable even in fixed resource environments. 

---

## Conclusion

RFID UIDs alone are majorly flawed with the ability to be easily spoofed and thus leading to insecure practices. Unfortunately, many real world security systems heavily rely on this flawed method to grant access into buildings, rooms, campuses, etc. This can lead to bad actors effortlessly spoofing authenticated UIDs to gain access into these restricted areas with little to no experience or skill. This project helps to demonstrate how simple and quick spoofing attacks are to get access into restricted areas when you are not authorized to.

As contactless access control becomes more common, no matter the scale of company, school, or apartments, systems must not ignore fundamental security flaws. Projects like this help bridge the gap between convenience and responsible, secure design. Allowing developers and students to think critically about system weaknesses and how to address them correctly.
