# Tell me about Atlantis

Atlantis (formally "The Momo") is a lake bed mapping system for impossible-to-reach places. The project underwent a major strategic pivot from underwater drone to surface boat with towed probe - problem-solving and adaptation in hardware development.

Started as an ambitious underwater drone using Raspberry Pi 4 for processing and Pi Pico for real-time sensor control. Original design included four brushless motors, IMU sensors, pressure sensors, ultrasonic obstacle detection, and underwater camera. But I realized waterproofing at depth, underwater communication, and safe recovery created overwhelming challenges.

For the actual goal of mapping lake beds, a surface boat with towed probe offered superior advantages. The current system is a remote-controlled surface boat towing a weighted probe with eight ultrasonic sensors in hemispherical array. GPS positioning and winch system control probe depth. Probe sends mapping data via LoRa long-range communication. Creates highly accurate 3D maps at a fraction of professional equipment costs.

Professional equipment costs $50,000 to $200,000 with plus-or-minus 10-50 centimeter accuracy. My system aims for plus-or-minus 1-2 centimeter accuracy at $500 to $2,000 cost. Eight ultrasonic sensors covering a hemisphere provide extremely dense point cloud data. Stopping the boat at measurement points eliminates motion artifacts.

The strategic pivot - recognizing when an approach isn't working and changing direction. The new system is simpler, more reliable, better suited to the actual goal.

Atlantis covers hardware integration beyond web development - LoRa communication, GPS positioning, winch control, ultrasonic sensor arrays, 3D printing, embedded systems, RF protocols, spatial data processing.

---

**emotion:** happy
**suggestions:**
- Tell me about a project that failed
- How do you approach project scoping?
- Why do you want to work at a startup?
- Tell me about your hardware experience
- How do you approach problem-solving?
- What projects have you built?

