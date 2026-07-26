#!/usr/bin/env python3
"""
Envoie chaque jour sur Telegram UNE idee de video POV (en francais) sur une
opportunite business (dropshipping / side hustle), avec un script pret a lire.
100% GRATUIT : aucune cle IA, aucun quota. Rotation deterministe sur la date,
2 idees differentes par jour (matin / apres-midi via RUN_SLOT).
"""

import os
import sys
import json
import datetime
import urllib.request
import urllib.error

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
TELEGRAM_LIMIT = 4096

BANK = [
    {
        "titre": "Le projecteur galaxie qui transforme une chambre",
        "lien": "https://www.tiktok.com/search?q=galaxy%20projector",
        "opp": [
            "Produit visuel effet 'wow' : la demo vend toute seule.",
            "Cout ~10-12$, revente 30-40$. Grosse marge sur achat impulsif.",
            "Dropshipping : aucun stock, la video fait la vente.",
        ],
        "hook": "POV : le produit a 12$ qui va imprimer de l'argent cette annee.",
        "corps": "Ce projecteur galaxie explose sur TikTok. Les gens filment leur chambre dans le noir, et boom, une galaxie au plafond. Tu l'achetes 12$, tu le revends 39$. Zero stock, tu fais du dropshipping et une seule bonne video peut en ecouler des centaines.",
        "cta": "Abonne-toi, je lache un produit gagnant chaque jour.",
        "hashtags": "#dropshipping #tiktokmademebuyit #produitgagnant #ecommerce #sidehustle #shopify",
        "astuce": "Dis les chiffres a voix haute (12$ -> 39$) en les affichant a l'ecran des la 1ere seconde.",
    },
    {
        "titre": "La lampe coucher de soleil (sunset lamp)",
        "lien": "https://www.tiktok.com/search?q=sunset%20lamp",
        "opp": [
            "Produit deco tendance, parfait pour photos/reels esthetiques.",
            "Cout ~6-9$, revente 25-30$.",
            "Cible : etudiants, deco chambre, createurs de contenu.",
        ],
        "hook": "POV : la lampe a 8$ que tout TikTok s'arrache.",
        "corps": "La sunset lamp projette un vrai coucher de soleil sur ton mur. Les gens l'utilisent pour leurs selfies et leurs reels. Tu l'as a 8$, tu la vends 27$. Montre juste l'ambiance qu'elle cree : la deco se vend a l'emotion, pas au discours.",
        "cta": "Follow pour le produit du jour, gratuit.",
        "hashtags": "#dropshipping #sunsetlamp #decochambre #produitgagnant #ecommerce #aesthetic",
        "astuce": "Filme un avant/apres : piece normale -> piece baignee de lumiere orange.",
    },
    {
        "titre": "Le mini-blender portable rechargeable",
        "lien": "https://www.tiktok.com/search?q=portable%20blender",
        "opp": [
            "Resout un probleme : smoothie n'importe ou (sport, bureau, voyage).",
            "Cout ~9-13$, revente 30-45$.",
            "Angle sante/fitness = audience large et qui achete.",
        ],
        "hook": "POV : le gadget qui se vend tout seul aux gens du fitness.",
        "corps": "Un blender qui tient dans un sac et se recharge en USB. Tu filmes juste : tu mets fruits + eau, tu appuies, smoothie pret en 20 secondes. Les gens fitness adorent. 12$ a l'achat, 39$ a la revente.",
        "cta": "Abonne-toi, un produit gagnant par jour.",
        "hashtags": "#dropshipping #fitness #smoothie #produitgagnant #ecommerce #tiktokmademebuyit",
        "astuce": "La demo satisfaisante (fruits qui tournent) = fort taux de retention. Montre-la en gros plan.",
    },
    {
        "titre": "Le correcteur de posture magnetique",
        "lien": "https://www.tiktok.com/search?q=posture%20corrector",
        "opp": [
            "Probleme reel : dos vouté a cause du telephone/PC.",
            "Cout ~5-8$, revente 25-35$.",
            "Angle sante = achat 'necessite', pas juste impulsif.",
        ],
        "hook": "POV : tu passes 8h par jour vouté... voila le fix a 6$.",
        "corps": "Ce correcteur de posture se porte sous les vetements et te force a te tenir droit. Enorme sur TikTok cote 'self-improvement'. Tu l'as a 6$, tu le vends 29$. Filme le avant/apres posture : c'est ca qui convertit.",
        "cta": "Follow, je poste un produit qui cartonne chaque jour.",
        "hashtags": "#dropshipping #posture #santedos #produitgagnant #selfimprovement #ecommerce",
        "astuce": "Montre-toi vouté puis droit. Le contraste visuel = le hook.",
    },
    {
        "titre": "L'aspirateur anti-poils pour animaux",
        "lien": "https://www.tiktok.com/search?q=pet%20hair%20remover",
        "opp": [
            "Cible enorme et fidele : les proprietaires d'animaux.",
            "Cout ~7-11$, revente 28-38$.",
            "Videos 'satisfaisantes' = viralite quasi garantie.",
        ],
        "hook": "POV : le produit qui rend accros les proprietaires de chats.",
        "corps": "Ce rouleau/aspi retire les poils du canape en un passage. Le contenu 'nettoyage satisfaisant' explose. 9$ a l'achat, 32$ a la revente. Filme juste le canape plein de poils -> propre en 3 secondes.",
        "cta": "Abonne-toi pour le produit gagnant du jour.",
        "hashtags": "#dropshipping #animaux #chat #chien #produitgagnant #satisfying",
        "astuce": "Le 'before/after' en gros plan est ta meilleure arme. Zero blabla, juste le resultat.",
    },
    {
        "titre": "Les bandes LED connectees pour chambre",
        "lien": "https://www.tiktok.com/tag/ledlights",
        "opp": [
            "Best-seller intemporel, surtout aupres des jeunes.",
            "Cout ~6-10$, revente 22-32$.",
            "Contenu 'room transformation' = millions de vues.",
        ],
        "hook": "POV : le produit deco a 8$ que chaque ado veut.",
        "corps": "Des LED qui changent de couleur pilotables au telephone. Le format 'transformation de chambre' cartonne depuis des annees. 8$ a l'achat, 27$ a la revente. Montre la chambre qui change de couleur au rythme de la musique.",
        "cta": "Follow, un produit gagnant chaque jour.",
        "hashtags": "#dropshipping #ledlights #decochambre #produitgagnant #roomtransformation #ecommerce",
        "astuce": "Synchronise le changement de couleur avec un son tendance = boost de l'algo.",
    },
    {
        "titre": "Le support telephone magnetique voiture",
        "lien": "https://www.tiktok.com/search?q=magnetic%20phone%20mount",
        "opp": [
            "Achat utile du quotidien pour tout conducteur.",
            "Cout ~4-7$, revente 20-28$.",
            "Marche gigantesque : tout le monde a une voiture + un tel.",
        ],
        "hook": "POV : le petit gadget voiture qui rapporte gros.",
        "corps": "Un support magnetique ultra-puissant qui tient le telephone d'une main. Simple, utile, achat impulsif. 5$ a l'achat, 24$ a la revente. Montre le 'clac' magnetique satisfaisant en gros plan.",
        "cta": "Abonne-toi pour le produit du jour.",
        "hashtags": "#dropshipping #cargadgets #accessoirevoiture #produitgagnant #ecommerce #tiktokmademebuyit",
        "astuce": "Filme le geste une main = montre a quel point c'est pratique en conduisant (a l'arret).",
    },
    {
        "titre": "Le roller visage en glace (skincare)",
        "lien": "https://www.tiktok.com/search?q=ice%20roller%20face",
        "opp": [
            "Niche beaute/skincare = audience qui depense.",
            "Cout ~4-6$, revente 18-26$.",
            "Routine matinale filmable = contenu infini.",
        ],
        "hook": "POV : le secret skincare a 5$ des filles sur TikTok.",
        "corps": "Un roller que tu mets au congelo puis sur le visage : degonfle, reveille la peau. La beaute cartonne en video. 5$ a l'achat, 22$ a la revente. Integre-le dans une routine 'get ready with me'.",
        "cta": "Follow pour un produit gagnant par jour.",
        "hashtags": "#dropshipping #skincare #beaute #produitgagnant #grwm #ecommerce",
        "astuce": "Format 'GRWM' (prepare-toi avec moi) : le produit apparait naturellement, ca vend sans vendre.",
    },
    {
        "titre": "La mini-imprimante photo/thermique",
        "lien": "https://www.tiktok.com/search?q=mini%20printer",
        "opp": [
            "Produit 'gadget mignon' tres partageable.",
            "Cout ~12-16$, revente 35-50$.",
            "Cible : etudiants, journaling, scrapbooking, notes.",
        ],
        "hook": "POV : la mini-imprimante a 14$ qui devient virale.",
        "corps": "Elle imprime photos et notes depuis le tel, sans encre. Enorme cote 'aesthetic' et etudes. 14$ a l'achat, 44$ a la revente. Filme l'impression d'une photo memo en direct : c'est hypnotique.",
        "cta": "Abonne-toi, produit gagnant chaque jour.",
        "hashtags": "#dropshipping #miniprinter #aesthetic #produitgagnant #etudiant #ecommerce",
        "astuce": "Montre un usage concret (coller la photo dans un journal) pour declencher le desir.",
    },
    {
        "titre": "Les gadgets de cuisine qui font gagner du temps",
        "lien": "https://www.tiktok.com/tag/kitchengadgets",
        "opp": [
            "Categorie infinie : coupe-legumes, presse, etc.",
            "Cout ~5-10$, revente 20-30$.",
            "Videos 'satisfaisantes' + 'hack cuisine' = viralite.",
        ],
        "hook": "POV : le gadget cuisine a 7$ que tout le monde va vouloir.",
        "corps": "Un coupe-legumes qui fait le travail en 5 secondes. Le contenu 'hack cuisine satisfaisant' marche a tous les coups. 7$ a l'achat, 26$ a la revente. Filme juste la decoupe rapide et nette.",
        "cta": "Follow pour le produit gagnant du jour.",
        "hashtags": "#dropshipping #kitchengadgets #hackcuisine #produitgagnant #satisfying #ecommerce",
        "astuce": "Gros plan + son 'ASMR' de la decoupe = retention maximale.",
    },
    {
        "titre": "L'objectif macro/grand-angle pour telephone",
        "lien": "https://www.tiktok.com/search?q=phone%20camera%20lens",
        "opp": [
            "Cible : createurs de contenu (marche qui explose).",
            "Cout ~6-10$, revente 25-35$.",
            "Demo visuelle immediate = fort taux de conversion.",
        ],
        "hook": "POV : l'accessoire a 8$ qui ameliore ta camera de tel.",
        "corps": "Un objectif clipsable qui transforme les photos du telephone (macro, grand-angle). Les createurs adorent. 8$ a l'achat, 29$ a la revente. Montre un avant/apres photo cote a cote.",
        "cta": "Abonne-toi, un produit gagnant par jour.",
        "hashtags": "#dropshipping #photographie #createurdecontenu #produitgagnant #ecommerce #gadget",
        "astuce": "Le split-screen avant/apres photo est le hook le plus efficace ici.",
    },
    {
        "titre": "La veste/gilet chauffant USB",
        "lien": "https://www.tiktok.com/search?q=heated%20vest",
        "opp": [
            "Produit saisonnier tres fort en automne/hiver.",
            "Cout ~15-22$, revente 45-65$.",
            "Angle confort/outdoor = panier moyen eleve.",
        ],
        "hook": "POV : le produit d'hiver qui se vend 3x son prix.",
        "corps": "Un gilet qui chauffe en quelques secondes via batterie USB. Parfait pour l'hiver, le sport en exterieur, les gens frileux. 20$ a l'achat, 59$ a la revente. Montre les zones qui chauffent.",
        "cta": "Follow pour le produit gagnant du jour.",
        "hashtags": "#dropshipping #hiver #outdoor #produitgagnant #ecommerce #tiktokmademebuyit",
        "astuce": "Publie ce type de produit AVANT la saison froide pour surfer la demande montante.",
    },
    {
        "titre": "Le print-on-demand (t-shirts sans stock)",
        "lien": "https://www.youtube.com/results?search_query=print+on+demand+2026",
        "opp": [
            "Zero stock : le produit est imprime a la commande.",
            "Marge 8-15$ par t-shirt, 100% en ligne.",
            "Outils gratuits : Canva pour le design, boutique auto.",
        ],
        "hook": "POV : tu vends des t-shirts sans jamais en toucher un seul.",
        "corps": "Le print-on-demand : tu crees un design sur Canva, tu le mets sur une boutique, et un partenaire imprime + expedie a chaque vente. Tu ne payes que quand tu vends. Trouve une niche (chats, gym, metiers) et fais du contenu.",
        "cta": "Abonne-toi, une idee de business par jour.",
        "hashtags": "#printondemand #businessenligne #sidehustle #ecommerce #entrepreneur #revenupassif",
        "astuce": "Attaque une micro-niche precise ('cadeau infirmiere') plutot qu'un theme large : moins de concurrence.",
    },
    {
        "titre": "La chaine YouTube faceless (sans montrer ton visage)",
        "lien": "https://www.youtube.com/results?search_query=faceless+youtube+automation",
        "opp": [
            "Aucune camera : voix off + images/videos libres.",
            "Monetisation pub + affiliation + produits.",
            "Outils IA pour script, voix et montage.",
        ],
        "hook": "POV : tu montes une chaine YouTube sans jamais te filmer.",
        "corps": "Les chaines 'faceless' (faits, top 10, histoires) cartonnent. Tu ecris un script, une IA fait la voix, tu montes avec des visuels libres de droits. Une video peut rapporter des mois via la pub. La cle : un theme rentable (finance, tech, histoire).",
        "cta": "Follow pour une idee de revenu chaque jour.",
        "hashtags": "#faceless #youtubeautomation #sidehustle #revenupassif #businessenligne #ia",
        "astuce": "Choisis une niche a fort CPM (finance, business, tech) : la meme vue rapporte plus.",
    },
    {
        "titre": "Les templates Notion a vendre",
        "lien": "https://www.youtube.com/results?search_query=sell+notion+templates",
        "opp": [
            "Produit digital : cree une fois, vends a l'infini.",
            "Zero cout de production, marge quasi 100%.",
            "Plateformes toutes pretes pour vendre.",
        ],
        "hook": "POV : tu crees UN fichier et tu le vends 1000 fois.",
        "corps": "Les gens payent pour des templates Notion (budget, productivite, planning). Tu en crees un bon, tu le mets en vente, et chaque copie vendue est pur profit. Fais des videos qui montrent le template en action.",
        "cta": "Abonne-toi, une idee business par jour.",
        "hashtags": "#notion #produitdigital #sidehustle #revenupassif #businessenligne #productivite",
        "astuce": "Offre un mini-template gratuit pour capter des abonnes, puis vends la version complete.",
    },
    {
        "titre": "L'agence de contenu IA (TikTok faceless pour marques)",
        "lien": "https://www.youtube.com/results?search_query=ai+faceless+tiktok+agency",
        "opp": [
            "Tu vends un service, pas un produit : cash rapide.",
            "Les commerces veulent du contenu mais n'ont pas le temps.",
            "Outils IA = tu produis vite et en volume.",
        ],
        "hook": "POV : tu factures des marques pour des videos que l'IA t'aide a faire.",
        "corps": "Beaucoup de petites entreprises veulent des TikTok mais ne savent pas les faire. Tu proposes un forfait mensuel (ex: 20 videos/mois). Avec les outils IA, tu produis vite. Un seul client peut te rapporter plusieurs centaines par mois.",
        "cta": "Follow pour une idee de revenu par jour.",
        "hashtags": "#agencecontenu #ia #sidehustle #freelance #businessenligne #tiktok",
        "astuce": "Fais 2-3 videos gratuites pour un premier client-temoin, puis utilise ce resultat pour vendre.",
    },
    {
        "titre": "Le UGC creator (contenu pour marques)",
        "lien": "https://www.youtube.com/results?search_query=ugc+creator+2026",
        "opp": [
            "Pas besoin d'audience : tu vends des videos aux marques.",
            "50-150$ par video UGC, depuis ton telephone.",
            "Demande enorme : les marques en consomment sans arret.",
        ],
        "hook": "POV : tu es paye pour filmer des produits chez toi, sans audience.",
        "corps": "Le UGC, c'est creer des videos authentiques 'type client' que les marques utilisent en pub. Pas besoin d'etre connu. Tu montes un petit portfolio, tu demarches des marques, et tu factures a la video. Ton telephone suffit.",
        "cta": "Abonne-toi, une idee business chaque jour.",
        "hashtags": "#ugc #ugccreator #sidehustle #freelance #businessenligne #createurdecontenu",
        "astuce": "Ton portfolio = 3 videos de produits que tu possedes deja. Commence sans attendre un client.",
    },
    {
        "titre": "Les produits digitaux (ebooks / guides)",
        "lien": "https://www.youtube.com/results?search_query=sell+digital+products+2026",
        "opp": [
            "Cree une fois, vends a l'infini, marge ~100%.",
            "Tu monetises un savoir que tu as deja.",
            "Livraison automatique, zero logistique.",
        ],
        "hook": "POV : ton savoir vaut de l'argent, meme pendant que tu dors.",
        "corps": "Transforme une competence (fitness, finance, langue, montage) en guide PDF ou mini-formation. Tu le crees une fois et chaque vente est automatique. Fais des videos 'valeur', puis vends le guide complet a ceux qui en veulent plus.",
        "cta": "Follow pour une idee de revenu par jour.",
        "hashtags": "#produitdigital #ebook #revenupassif #sidehustle #businessenligne #entrepreneur",
        "astuce": "Poste 3 conseils gratuits en video, puis 'la methode complete est dans le guide'. Simple et efficace.",
    },
    {
        "titre": "L'affiliation (vendre les produits des autres)",
        "lien": "https://www.youtube.com/results?search_query=affiliate+marketing+for+beginners+2026",
        "opp": [
            "Aucun produit a creer : tu touches une commission.",
            "Tu recommandes, tu es paye a chaque vente.",
            "Combine parfaitement avec du contenu 'review'.",
        ],
        "hook": "POV : tu gagnes une commission sans creer aucun produit.",
        "corps": "L'affiliation : tu recommandes un produit avec ton lien, et tu touches une commission a chaque vente. Fais des videos 'top 5 outils' ou 'produits que j'utilise' avec tes liens. Aucun stock, aucun SAV.",
        "cta": "Abonne-toi, une idee business chaque jour.",
        "hashtags": "#affiliation #affiliatemarketing #revenupassif #sidehustle #businessenligne #entrepreneur",
        "astuce": "Recommande UNIQUEMENT ce que tu utilises vraiment : la confiance = le taux de conversion.",
    },
    {
        "titre": "Le dropshipping teste par mini-budget pub",
        "lien": "https://www.youtube.com/results?search_query=dropshipping+2026+beginners",
        "opp": [
            "Zero stock, tu testes des produits avec un petit budget.",
            "Un seul produit gagnant peut tout changer.",
            "Boutique montable en une journee.",
        ],
        "hook": "POV : tu testes 3 produits cette semaine, un peut exploser.",
        "corps": "Le dropshipping en 2026 : tu montes une boutique, tu testes des produits avec du contenu organique (TikTok gratuit) avant de mettre de la pub. Tu gardes ceux qui marchent, tu coupes le reste. Teste vite, coupe vite.",
        "cta": "Follow pour un produit/idee chaque jour.",
        "hashtags": "#dropshipping #ecommerce #shopify #sidehustle #businessenligne #entrepreneur",
        "astuce": "Teste en organique (video gratuite) avant de payer de la pub. Tu economises et tu valides la demande.",
    },
    {
        "titre": "Les templates Canva a vendre",
        "lien": "https://www.youtube.com/results?search_query=sell+canva+templates",
        "opp": [
            "Produit digital, marge quasi 100%.",
            "Tout le monde veut des visuels prets a l'emploi.",
            "Cree sur Canva (gratuit), vends en boucle.",
        ],
        "hook": "POV : tu vends des designs Canva pendant ton sommeil.",
        "corps": "Beaucoup de gens veulent de beaux visuels mais ne savent pas les faire. Tu crees des packs de templates (posts Insta, CV, presentations) sur Canva et tu les vends. Une creation, des ventes illimitees.",
        "cta": "Abonne-toi, une idee de revenu par jour.",
        "hashtags": "#canva #produitdigital #sidehustle #revenupassif #businessenligne #design",
        "astuce": "Vends des PACKS (ex: 30 templates Insta) plutot qu'a l'unite : panier plus eleve.",
    },
    {
        "titre": "La revente (thrift flipping / seconde main)",
        "lien": "https://www.youtube.com/results?search_query=reselling+flipping+2026",
        "opp": [
            "Faible mise de depart, marges elevees.",
            "Tu achetes bas (friperie, vide-grenier), tu vends haut.",
            "Marche seconde main en pleine explosion.",
        ],
        "hook": "POV : tu transformes 5$ de friperie en 40$.",
        "corps": "Le flipping : tu deniches des pieces sous-cotees (vetements de marque, objets) et tu les revends en ligne au vrai prix. Faible investissement, apprentissage rapide de ce qui se vend. Documente tes trouvailles : le 'thrift haul' cartonne.",
        "cta": "Follow pour une idee business chaque jour.",
        "hashtags": "#reselling #flipping #secondemain #sidehustle #businessenligne #thrift",
        "astuce": "Filme le 'combien je l'ai paye vs combien je l'ai vendu' : le contraste chiffre accroche.",
    },
    {
        "titre": "La gestion de reseaux sociaux (SMMA light)",
        "lien": "https://www.youtube.com/results?search_query=social+media+manager+2026",
        "opp": [
            "Service a forte demande : les commerces manquent de temps.",
            "Revenu recurrent (forfait mensuel).",
            "Zero produit, tu vends ton temps + tes competences.",
        ],
        "hook": "POV : tu geres l'Insta d'un commerce et tu factures chaque mois.",
        "corps": "Beaucoup de petits commerces n'ont ni le temps ni l'envie de gerer leurs reseaux. Tu proposes un forfait : X posts + reponses aux messages par mois. 2-3 clients = un vrai revenu recurrent. Commence par un commerce local.",
        "cta": "Abonne-toi, une idee de revenu par jour.",
        "hashtags": "#smma #reseauxsociaux #freelance #sidehustle #businessenligne #entrepreneur",
        "astuce": "Propose le 1er mois a prix reduit pour prouver ta valeur, puis passe au tarif plein.",
    },
    {
        "titre": "Le copywriting / redaction pour marques",
        "lien": "https://www.youtube.com/results?search_query=copywriting+beginners+2026",
        "opp": [
            "Competence payante : les mots qui vendent.",
            "Aucun investissement, juste ton cerveau + un PC.",
            "Emails, pages de vente, pubs : demande constante.",
        ],
        "hook": "POV : tu ecris des mots et les marques te payent cher.",
        "corps": "Le copywriting, c'est ecrire pour vendre (emails, pages, pubs). Les entreprises payent bien car un bon texte = plus de ventes. Tu apprends les bases, tu fais quelques exemples, et tu demarches. Un skill que tu gardes a vie.",
        "cta": "Follow pour une idee business chaque jour.",
        "hashtags": "#copywriting #freelance #sidehustle #businessenligne #ecriture #entrepreneur",
        "astuce": "Reecris la page d'un commerce local gratuitement comme demo : ton meilleur argument de vente.",
    },
    {
        "titre": "Les voix off IA (chaines automatisees)",
        "lien": "https://www.youtube.com/results?search_query=ai+voiceover+channel",
        "opp": [
            "Produis du contenu audio/video sans micro ni voix.",
            "Combine avec YouTube faceless pour monetiser.",
            "Outils IA de plus en plus realistes.",
        ],
        "hook": "POV : tu lances une chaine sans jamais parler.",
        "corps": "Avec les voix IA, tu transformes un script en narration pro sans micro. Parfait pour des chaines de faits, d'histoires ou de tutos. Tu ecris, l'IA raconte, tu montes. Le volume + une bonne niche = de la pub et de l'affiliation.",
        "cta": "Abonne-toi, une idee de revenu par jour.",
        "hashtags": "#ia #voixoff #faceless #sidehustle #revenupassif #youtubeautomation",
        "astuce": "Reste sur un theme precis par chaine : l'algo te pousse mieux quand c'est coherent.",
    },
    {
        "titre": "La boutique Etsy de produits digitaux",
        "lien": "https://www.youtube.com/results?search_query=etsy+digital+products+2026",
        "opp": [
            "Trafic deja present sur la plateforme.",
            "Produits digitaux : livraison auto, marge ~100%.",
            "Invitations, plannings, stickers, imprimables.",
        ],
        "hook": "POV : tu vends des fichiers sur Etsy sans rien expedier.",
        "corps": "Sur Etsy, les imprimables (plannings, invitations, art mural) se vendent en telechargement. Tu crees une fois, la plateforme t'amene des acheteurs, la livraison est automatique. Fais du contenu qui montre tes designs.",
        "cta": "Follow pour une idee business chaque jour.",
        "hashtags": "#etsy #produitdigital #imprimable #sidehustle #revenupassif #businessenligne",
        "astuce": "Vise les evenements (mariage, rentree, fetes) : la demande est saisonniere et forte.",
    },
    {
        "titre": "L'agence de chatbots IA pour commerces",
        "lien": "https://www.youtube.com/results?search_query=ai+chatbot+agency+2026",
        "opp": [
            "Nouveau marche : les commerces veulent automatiser.",
            "Service a forte valeur = tarifs eleves.",
            "Outils no-code pour construire les bots.",
        ],
        "hook": "POV : tu installes un chatbot et tu factures 500$.",
        "corps": "Beaucoup de commerces perdent des clients faute de reponses rapides. Tu montes un chatbot (no-code) qui repond aux questions et prend les reservations. Tu factures l'installation + un abonnement. Un skill tres demande et peu concurrentiel.",
        "cta": "Abonne-toi, une idee de revenu par jour.",
        "hashtags": "#ia #chatbot #automatisation #sidehustle #businessenligne #entrepreneur",
        "astuce": "Cible un secteur precis (restos, salons) : tu reutilises le meme bot et tu vends plus vite.",
    },
    {
        "titre": "Le freelance de services IA (Fiverr / Upwork)",
        "lien": "https://www.youtube.com/results?search_query=ai+freelance+services+2026",
        "opp": [
            "Demarrage immediat, zero investissement.",
            "Vends un service concret : montage, design, redaction.",
            "L'IA te rend plus rapide = plus de missions.",
        ],
        "hook": "POV : tu proposes un service IA et les commandes tombent.",
        "corps": "Sur les plateformes freelance, propose un service clair (miniatures, montage court, redaction, traduction) booste a l'IA. Tu livres vite et bien, tu accumules les avis, tu montes tes prix. Le plus dur c'est le 1er client.",
        "cta": "Follow pour une idee business chaque jour.",
        "hashtags": "#freelance #ia #sidehustle #fiverr #businessenligne #revenu",
        "astuce": "Une seule offre ultra-claire au depart > 10 services flous. La specialisation attire.",
    },
    {
        "titre": "Le tunnel 'contenu gratuit -> produit payant'",
        "lien": "https://www.youtube.com/results?search_query=content+to+cash+creator+business",
        "opp": [
            "Transforme des vues en clients, pas juste en likes.",
            "Marche pour n'importe quelle niche.",
            "Base de tout business de createur durable.",
        ],
        "hook": "POV : tes vues ne rapportent rien... tant que tu ne fais pas ca.",
        "corps": "Les vues ne payent pas les factures. Le systeme : contenu gratuit qui apporte de la valeur -> tu captes des abonnes -> tu leur proposes un produit (guide, service, affiliation). Chaque video doit avoir un but.",
        "cta": "Abonne-toi, une strategie business par jour.",
        "hashtags": "#createur #businessenligne #sidehustle #monetisation #entrepreneur #strategie",
        "astuce": "Ajoute UN appel a l'action clair par video (commente un mot, clique le lien). Sans ca, zero conversion.",
    },
]


def fail(msg):
    print(f"ERREUR: {msg}", file=sys.stderr)
    sys.exit(1)


def check_env():
    missing = [n for n, v in [("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)] if not v]
    if missing:
        fail("Secrets manquants: " + ", ".join(missing))


def pick_entry():
    slot = 1 if os.environ.get("RUN_SLOT", "").strip().lower() == "afternoon" else 0
    idx = (datetime.date.today().toordinal() * 2 + slot) % len(BANK)
    return BANK[idx]


def format_pack(e):
    opp = "\n".join(f"- {x}" for x in e["opp"])
    return (
        "🎥 LA VIDEO A REFAIRE AUJOURD'HUI\n"
        f"{e['titre']}\n"
        f"👉 Exemples viraux en direct : {e['lien']}\n\n"
        "💡 L'OPPORTUNITE BUSINESS\n"
        f"{opp}\n\n"
        "🎬 TON SCRIPT POV (~35 sec)\n"
        f"HOOK (0-3s) : \"{e['hook']}\"\n"
        f"CORPS : \"{e['corps']}\"\n"
        f"CTA : \"{e['cta']}\"\n\n"
        "#️⃣ HASHTAGS\n"
        f"{e['hashtags']}\n\n"
        "📌 ASTUCE DE PUBLICATION\n"
        f"{e['astuce']}"
    )


def http_post_json(url, payload, headers, timeout=30):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        fail(f"HTTP {e.code} sur {url}: {e.read().decode('utf-8', errors='replace')}")
    except urllib.error.URLError as e:
        fail(f"Connexion echouee sur {url}: {e}")
    return {}


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    headers = {"Content-Type": "application/json"}
    parts = [text[i:i + TELEGRAM_LIMIT] for i in range(0, len(text), TELEGRAM_LIMIT)] or [text]
    for part in parts:
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": part, "disable_web_page_preview": True}
        resp = http_post_json(url, payload, headers)
        if not resp.get("ok"):
            fail("Envoi Telegram echoue: " + json.dumps(resp)[:1000])
    print("Pack envoye sur Telegram OK")


def main():
    check_env()
    pack = format_pack(pick_entry())
    print(pack)
    send_telegram(pack)


if __name__ == "__main__":
    main()
