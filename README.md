# pacman-pygame
# 🎮 Joc Pacman în Python (Pygame)

Acesta este un joc dezvoltat în Python 3 folosind biblioteca `pygame`, care implementează o versiune simplificată a jocului **Pacman**, cu mai multe nivele și o logică adaptată pentru un proiect educațional.

## 📋 Cerință

La rularea programului, în consolă va fi afișat un **labirint** de culoare gri, a cărui formă este aleasă de student. 

În cadrul acestui labirint sunt prezente următoarele elemente:
- 🟡 **Packman** – bulina galbenă, controlată de utilizator.
- 🔴 **4 inamici roșii** – de care utilizatorul trebuie să se ferească.
- 🟢 **4 fructe verzi** – care oferă puncte atunci când sunt colectate.
- 🟣 **Buline violet** – oferă putere temporară Packman-ului pentru a „mânca” inamicii roșii (care devin albaștri).

Scorul se calculează în funcție de:
- Fructele colectate.
- Timpul în care a fost parcurs nivelul.

---

## ⚙️ Funcționalități

✅ Desenarea labirintului și a punctelor:
- 1 punct galben (Packman)
- 4 puncte roșii (inamici)
- 4 puncte verzi (fructe)
- puncte gri (toate zonele accesibile ale labirintului)

✅ Redesenarea scenei în funcție de pozițiile actuale (efect de mișcare).

✅ Controlul Packman-ului cu săgețile:
- Dacă direcția aleasă lovește un perete, se ignoră.

✅ Deplasarea inamicilor roșii după o funcție aleatoare (`random`).

✅ Interacțiuni:
- Dacă Packman atinge o fructă, aceasta dispare și este generată alta.
- Dacă Packman atinge un inamic roșu → jocul se termină.
- Dacă Packman atinge o bulină violet → inamicii devin albaștri și pot fi consumați timp de 5 secunde.

✅ Pauză și reluare cu tasta `SPACE`.

✅ Afișarea scorului și a timpului în interfață.

✅ Trecerea automată la următorul nivel, cu un ecran de tranziție care afișează scorul și timpul.

---

## 🗺️ Nivele

- Jocul conține **3 nivele** cu hărți de dimensiuni diferite.
- Fiecare nivel este original și mai complex decât cel anterior.
- Nivelul este considerat complet când:
  - Packman trece peste toate punctele gri (zone accesibile).
  - Toate fructele sunt colectate.

---

## ▶️ Cum rulezi jocul

1. Asigură-te că ai instalat Python 3 și Pygame:
   ```bash
   pip install pygame
