Singleton - Am utilizat Singleton pentru a asigura că în cadrul clasei DatabaseConnector există o singură instanță a obiectului de bază db, garantând astfel accesul la o singură conexiune la baza de date în întreaga aplicație.

Builder - Am implementat șablonul Builder în cadrul clasei RentalsBuilder pentru a construi obiecte complexe de tip Rentals cu parametri opcionali, oferind o metodă flexibilă și ușor de utilizat pentru inițializarea acestor obiecte.

Factory - Am folosit șablonul Factory în clasa CarFactory pentru a crea obiecte de tip Cars, oferind o interfață comună pentru crearea diferitelor tipuri de mașini în cadrul aplicației.

Decorator - Am folosit șablonul Decorator în clasele CarDecorator, ChildSeat, GPS și RoofBag pentru a extinde funcționalitatea obiectelor de tip Car prin adăugarea de opțiuni suplimentare, cum ar fi scaun pentru copii, GPS sau sac de plafon, oferind astfel posibilitatea de personalizare a mașinilor în funcție de preferințele utilizatorilor.

Repository - Am utilizat șablonul Repository în clasa DatabaseFacade pentru a abstractiza interacțiunea cu baza de date și a oferi o interfață simplificată pentru accesul la date, ascunzând detaliile de implementare și permițând astfel gestionarea eficientă a operațiilor CRUD în cadrul aplicației.

Facade - Am aplicat șablonul Facade în clasa DatabaseFacade pentru a oferi o interfață simplificată și unificată pentru gestionarea operațiilor de bază pe baza de date, ascunzând detaliile complexe ale interacțiunii cu ORM-ul și oferind astfel un nivel de abstractizare și modularitate în cadrul aplicației noastre.

Observer - Am implementat șablonul Observer pentru a permite notificarea și actualizarea diferitelor părți ale aplicației în funcție de evenimente precum adăugarea unei noi mașini sau închirierea unei mașini.

State - Am utilizat șablonul State pentru a gestiona starea mașinilor în cadrul aplicației, permițându-ne să modificăm și să controlăm comportamentul mașinilor în funcție de starea lor (disponibilă sau închiriată)

Strategy - Am implementat șablonul Strategy în clasele StandardPricingStrategy și MonthlyPricingStrategy pentru a permite schimbarea dinamică a strategiei de calcul a prețului în funcție de durata închirierii unei mașini, oferind astfel flexibilitate în ajustarea politicii de prețuri în funcție de nevoile utilizatorilor.
