# FTC Elo Rating System  
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-blue)](https://ftcelo.vercel.app/)  
[![Creator Portfolio](https://img.shields.io/badge/Creator-Monish%20Saravana-orange)](https://monishsaravana.com/)


https://ftcelo.vercel.app/

## Overview  
A chess-inspired Elo rating system for FTC teams using match data from the FTC Scout API. Predict alliance strengths and compare team performance across events.

---

### Features  
1. **Team Elo Lookup**  
   Get current Elo ratings for any FTC team:  
   ```
   Team Number: 22012  
   Elo Rating: 1487  
   ```

2. **Match Predictor**  
   Compare Blue vs Red alliances:  
   ```
   Blue Alliance: 22012 + 18165  
   Red Alliance: 12345 + 67890  
   Predicted Winner: Blue (68% chance)  
   ```

3. **Event Normalization**  
   Adjusts ratings based on regional competition intensity using world record event benchmarks.

---

### Technologies Used  
- Python (Elo calculation engine)  
- HTML/CSS (Frontend interface)  
- FTC Scout API (Match data)  
- Vercel (Hosting)  
- Flash (Server-side rendering)  


---

### Disclaimer ⚠️  
This is an **unofficial** tool not affiliated with FIRST Tech Challenge. Ratings are algorithmic estimates only - use at your own discretion.

---

### Methodology  
1. Pulls match results from [FTC Scout](https://api.ftcscout.org/)  
2. Applies modified chess Elo formulas:  
   ```python
   # Point difference weighting
   math.pow(math.log10(1 + abs(teamScore/2 - opposingScore/2)), 2)
   ```
3. Normalizes for event strength using:  
   ```python
   0.51 * math.log((-(highscore - region_score)/highscore) + 1, 10) + 1
   ```

---

### Creator  
Monish Saravana (FTC Team 22012)  
[Portfolio](https://monishsaravana.com/) | [FTC Events](https://events.ftcscout.org/team/22012)  

---
