#!/usr/bin/env python3
"""Builds the static site in English (/) and Italian (/it/). Run: python3 build.py

Edit the copy in STRINGS below, then rebuild and commit the generated HTML.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://marcogaroglio-online.github.io/melian-site/"
# Where people reach us from the support page.
CONTACT_URL = "https://github.com/marcogaroglio-online/melian-site/issues/new"
UPDATED = {"en": "17 October 2026", "it": "17 ottobre 2026"}

ICON = {
    "moon": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14.5 3.2a8.6 8.6 0 1 0 6.3 12.6A7.2 7.2 0 0 1 14.5 3.2Z"/><path d="m18.6 2.5.5 1.6 1.6.5-1.6.5-.5 1.6-.5-1.6-1.6-.5 1.6-.5Z"/><path d="m21.4 7.4.3 1 1 .3-1 .3-.3 1-.3-1-1-.3 1-.3Z"/></svg>',
    "bottle": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 2h6v2.2l1.4 2.3c.4.6.6 1.3.6 2V20a2 2 0 0 1-2 2H9a2 2 0 0 1-2-2V8.5c0-.7.2-1.4.6-2L9 4.2Z"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.5S5 10 5 14.6A7 7 0 0 0 19 14.6C19 10 12 2.5 12 2.5Z"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.5 3.5S8 2.6 4.8 9.6c-1.6 3.5-.4 7 1.6 8.6C9.7 13 13.5 10.6 16 9.6c-3.4 2-6.8 5.4-8.6 9.6 3.6 1.4 8.3.6 10.8-3.6 2.6-4.3 2.3-12.1 2.3-12.1Z"/></svg>',
    "half": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3S5.5 10.2 5.5 14.6a6.5 6.5 0 0 0 13 0C18.5 10.2 12 3 12 3Z"/><path fill="currentColor" stroke="none" d="M5.6 14h12.8a6.5 6.5 0 0 1-12.8 0Z"/></svg>',
    "bell": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a6 6 0 0 0-6 6v4.3L4.3 15.6A1 1 0 0 0 5.2 17h13.6a1 1 0 0 0 .9-1.4L18 12.3V8a6 6 0 0 0-6-6Zm-2.6 16.5a2.7 2.7 0 0 0 5.2 0Z"/></svg>',
    "apple": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.4 12.6c0-2.4 2-3.5 2-3.6a4.3 4.3 0 0 0-3.4-1.8c-1.4-.1-2.8.9-3.5.9s-1.8-.8-3-.8a4.5 4.5 0 0 0-3.8 2.3c-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2 0 1.6-.7 3-.7s1.8.7 3 .7c1.3 0 2.1-1.1 2.8-2.3a10 10 0 0 0 1.3-2.6 3.9 3.9 0 0 1-2.5-3.7ZM14.2 5.6A4 4 0 0 0 15.1 2.6a4.1 4.1 0 0 0-2.7 1.4 3.8 3.8 0 0 0-1 2.9 3.4 3.4 0 0 0 2.8-1.3Z"/></svg>',
}

STRINGS = {
    "en": {
        "lang_name": "English", "other_lang": "Italiano", "other_code": "it",
        "title": "Melian: a calm baby feeding and nappy tracker for iPhone",
        "description": "Log feeds and nappies in one tap, get a loud reminder when the next feed is due, and share everything live with your partner. No accounts, no ads, no tracking.",
        "nav_story": "How it works", "nav_philosophy": "Philosophy", "nav_privacy": "Privacy", "nav_support": "Support",
        "eyebrow": "For the first months",
        "h1": ["Every feed.", "Every nappy.", "Calmly kept."],
        "lead": "Melian is a quiet iPhone app for logging your baby's feeds and nappies in one tap, reminding you when the next feed is due, and keeping both parents in step. No accounts, no ads, nothing to set up.",
        "badge_small": "Coming soon on the", "badge": "App Store",
        "ghost": "Read the philosophy",
        "scroll": "Scroll",
        "try": "Try it: tap the buttons on the phone.",
        "phone_name": "Vittoria", "phone_age": "5 weeks old", "since": "Since last feed", "next": "next",
        "formula": "Formula", "feeds": "Feeds", "wet": "Wet", "dirty": "Dirty",
        "feed": "Feed", "repeat": "Tap to log 110 ml", "both": "Both", "timeline": "Timeline",
        "feed_row": "Feed · 110 ml", "wet_row": "Wet nappy", "dirty_row": "Dirty nappy", "both_row": "Wet & dirty",
        "alarm_title": "Time for a feed", "alarm_sub": "Vittoria · last fed 3h ago", "snooze": "Snooze", "fed": "Fed",
        "partner_name": "Vittoria", "partner_age": "On your partner's iPhone",
        "chapters": [
            ("Log it in one tap.", "Half asleep, one hand on the bottle. Feed, wet, dirty: one tap each, from the app, a widget, the Lock Screen or Siri. Melian remembers the last amount, so most feeds take a second."),
            ("Loud when it matters.", "After each feed Melian sets the next one. When it's time it rings like an alarm, even on silent, and it never logs a feed on its own. Meanwhile the countdown waits on your Lock Screen and in the Dynamic Island."),
            ("Two phones, one story.", "Invite your partner and both iPhones see the same day, live. Whoever is up at 3 a.m. knows what happened at midnight without waking anyone."),
            ("Guidance, not judgement.", "Soft rings show the day against indicative ranges for your baby's age and weight, with the source one tap away. A reference, never a score, and never a replacement for your midwife or doctor."),
        ],
        "statement": ["Less noise.", "More sleep."],
        "ph_eyebrow": "Philosophy",
        "ph_title": "Made by a tired parent, for tired parents.",
        "ph_lead": "Melian started as a tool for one family's nights. Every decision since follows the same few rules.",
        "principles": [
            ("One tap, or it doesn't belong.", "If something takes two steps at 3 a.m., it gets redesigned until it takes one."),
            ("Calm by default.", "Soft colours, few words, no streaks and no badges. The app stays quiet until the moment it shouldn't."),
            ("Your data stays yours.", "No accounts and no servers of ours. Everything lives on your iPhone and in your own iCloud."),
            ("It never decides for you.", "Reminders ring, but they never log a feed by themselves. You stay in charge of what happened."),
            ("Guidance with sources.", "Every number comes from published health guidance, and the reference is shown. Indicative, never prescriptive."),
            ("Made for two.", "Parenting is shared, so the app is too. Both phones see the same day, in real time."),
        ],
        "pv_eyebrow": "Privacy",
        "pv_title": "We never see your baby's data.",
        "pv_lead": "Melian has no accounts and no servers. Feeds, nappies and growth are stored on your iPhone and in your family's private iCloud, shared only with the partner you invite. We can't read it, sell it or lose it.",
        "pv_link": "Read the privacy policy",
        "dg_you": "Your iPhone", "dg_cloud": "Your iCloud", "dg_partner": "Partner's iPhone", "dg_us": "Melian, the developer", "dg_us_sub": "no access", "dg_private": "private, encrypted by Apple",
        "quote": "Melian began at 3 a.m., with a newborn, a bottle and a phone full of notes that didn't add up. I wanted something that felt like a calm hand on the shoulder: tell me when she last ate, remind me when she'll be hungry, and let me go back to sleep.",
        "cite": "Marco, father and maker of Melian",
        "end_title": "Coming soon to the App Store.",
        "end_lead": "Melian is being tested by a few families. It's for iPhone with iOS 26 or later, in English and Italian.",
        "footer_note": "Melian shows indicative guidance only and is not a medical device.",
        # privacy policy
        "pp_title": "Privacy policy", "pp_meta": "Last updated",
        "pp_summary": "<strong>Melian does not collect any personal data.</strong> Everything you record stays on your devices and in your own iCloud account. We, the developer, cannot see it.",
        "pp_body": """
<h2>Who we are</h2>
<p>Melian is made by Marco Mattia Garoglio, an independent developer in Italy (“we”). This policy covers the Melian app for iPhone and its widgets.</p>
<h2>What Melian stores, and where</h2>
<p>When you use Melian you may record your baby's name, birth date, sex, gestational age and an optional photo, along with feeds, nappy changes, notes and growth measurements, and the name you choose to show on your entries.</p>
<ul>
<li><strong>On your iPhone.</strong> This information is saved on your device so the app, widgets and Live Activity can show it.</li>
<li><strong>In your iCloud.</strong> If you are signed in to iCloud, Melian syncs it to the private database of your own iCloud account using Apple's CloudKit. It is processed by Apple under <a href="https://www.apple.com/legal/privacy/">Apple's privacy policy</a>. We have no access to your private iCloud data.</li>
<li><strong>With the people you invite.</strong> If you invite a partner from Settings, the data is shared with them through iCloud sharing. You can stop sharing at any time.</li>
<li><strong>In your backups.</strong> Melian writes a daily backup file to Files › On My iPhone › Melian. These files stay on your device unless you move or share them.</li>
</ul>
<h2>What we collect</h2>
<p>Nothing. Melian has no accounts, no analytics, no advertising, no tracking and no third-party SDKs. We do not sell, rent or share data, because we never receive it.</p>
<p>If you have chosen to share analytics with app developers in iOS settings, Apple may send us anonymous crash reports and usage statistics. These do not include the information you record in Melian.</p>
<h2>Reminders, alarms and Siri</h2>
<p>Feed reminders and alarms are scheduled on your iPhone. If you use Siri or Shortcuts with Melian, your request is handled by Apple.</p>
<h2>Children</h2>
<p>Melian is used by parents and caregivers to record information about their baby. It is not directed at children. Because we do not collect data, no information about any child ever reaches us.</p>
<h2>Your choices</h2>
<ul>
<li>To export your data, use Settings › Export data in the app.</li>
<li>To delete everything, delete Melian from your iPhone, then remove its data in iOS Settings › your name › iCloud › Manage Storage › Melian. A partner keeps their access until you stop sharing.</li>
</ul>
<p>Since we hold no personal data about you, there is nothing for us to access, correct or delete on your behalf. If you live in the EU or UK, you still have every right granted by the GDPR, and you can contact us with any question.</p>
<h2>Changes</h2>
<p>If this policy changes, we will update this page and the date above. A change that starts collecting data would need your consent in the app first.</p>
<h2>Contact</h2>
<p>Questions about privacy? See the <a href="support.html">support page</a>.</p>
""",
        # support
        "sp_title": "Support", "sp_lead": "Questions, problems or ideas? Every message is read by the person who makes Melian.",
        "sp_contact": "Write to us",
        "sp_contact_note": "Opens a short form on GitHub.",
        "faq_title": "Common questions",
        "faq": [
            ("How do I invite my partner?", "Open Settings › Invite partner and send the invitation with Messages, Mail or any app. Your partner opens it on their iPhone with Melian installed, and both phones show the same data from then on."),
            ("The alarm didn't ring. What should I check?", "In Melian, make sure Settings › Feed reminders › Remind me to feed and Loud alarm are on. Then check that alarms and notifications are allowed for Melian in iOS Settings. Settings › Test the alarm lets you hear it right away."),
            ("Does a reminder log a feed by itself?", "No. A reminder only tells you it's time. A feed is logged only when you or your partner tap Feed, in the app, on a widget or on the Live Activity."),
            ("Where is my data, and how do I back it up?", "On your iPhone and in your own iCloud. Melian also saves a daily backup in Files › On My iPhone › Melian, and Settings › Export data creates one whenever you want."),
            ("How do I delete everything?", "Delete Melian, then go to iOS Settings › your name › iCloud › Manage Storage › Melian and delete its data."),
            ("Are the feeding amounts medical advice?", "No. They are indicative ranges from published health guidance, shown with their source. Always follow your midwife, health visitor or doctor."),
            ("Which iPhones are supported?", "Any iPhone that runs iOS 26 or later."),
        ],
    },
    "it": {
        "lang_name": "Italiano", "other_lang": "English", "other_code": "en",
        "title": "Melian: poppate e pannolini, con calma, su iPhone",
        "description": "Registra poppate e pannolini con un tocco, ricevi una sveglia quando arriva la prossima poppata e condividi tutto in tempo reale con il partner. Senza account, pubblicità o tracciamento.",
        "nav_story": "Come funziona", "nav_philosophy": "Filosofia", "nav_privacy": "Privacy", "nav_support": "Assistenza",
        "eyebrow": "Per i primi mesi",
        "h1": ["Ogni poppata.", "Ogni pannolino.", "Con calma."],
        "lead": "Melian è un'app per iPhone, tranquilla, per registrare poppate e pannolini con un tocco, ricordarti quando arriva la prossima poppata e tenere entrambi i genitori allineati. Senza account, senza pubblicità, niente da configurare.",
        "badge_small": "Presto su", "badge": "App Store",
        "ghost": "Leggi la filosofia",
        "scroll": "Scorri",
        "try": "Provalo: tocca i pulsanti sul telefono.",
        "phone_name": "Vittoria", "phone_age": "5 settimane", "since": "Dall'ultima poppata", "next": "prossima",
        "formula": "Latte", "feeds": "Poppate", "wet": "Bagnati", "dirty": "Sporchi",
        "feed": "Poppata", "repeat": "Tocca per 110 ml", "both": "Entrambi", "timeline": "Cronologia",
        "feed_row": "Poppata · 110 ml", "wet_row": "Pannolino bagnato", "dirty_row": "Pannolino sporco", "both_row": "Bagnato e sporco",
        "alarm_title": "È ora della poppata", "alarm_sub": "Vittoria · ultima 3 ore fa", "snooze": "Posticipa", "fed": "Fatto",
        "partner_name": "Vittoria", "partner_age": "Sull'iPhone del partner",
        "chapters": [
            ("Un tocco, ed è registrato.", "Mezzo addormentato, una mano sul biberon. Poppata, bagnato, sporco: un tocco ciascuno, dall'app, da un widget, dalla schermata di blocco o con Siri. Melian ricorda l'ultima quantità, quindi quasi ogni poppata richiede un secondo."),
            ("Suona quando serve.", "Dopo ogni poppata Melian imposta la prossima. Quando è ora suona come una sveglia, anche in silenzioso, e non registra mai una poppata da sola. Nel frattempo il conto alla rovescia resta sulla schermata di blocco e nella Dynamic Island."),
            ("Due telefoni, una storia.", "Invita il partner e i due iPhone vedono la stessa giornata, in tempo reale. Chi è sveglio alle 3 sa cosa è successo a mezzanotte senza svegliare nessuno."),
            ("Indicazioni, non giudizi.", "Anelli morbidi mostrano la giornata rispetto a intervalli indicativi per età e peso, con la fonte a un tocco. Un riferimento, mai un punteggio, e mai un sostituto dell'ostetrica o del pediatra."),
        ],
        "statement": ["Meno rumore.", "Più sonno."],
        "ph_eyebrow": "Filosofia",
        "ph_title": "Fatta da un genitore stanco, per genitori stanchi.",
        "ph_lead": "Melian è nata per le notti di una famiglia. Ogni scelta da allora segue poche regole.",
        "principles": [
            ("Un tocco, o non serve.", "Se alle 3 di notte qualcosa richiede due passaggi, lo ridisegniamo finché ne basta uno."),
            ("Calma prima di tutto.", "Colori morbidi, poche parole, niente serie e niente badge. L'app resta silenziosa finché non deve farsi sentire."),
            ("I tuoi dati restano tuoi.", "Nessun account e nessun nostro server. Tutto vive sul tuo iPhone e nel tuo iCloud."),
            ("Non decide mai al posto tuo.", "I promemoria suonano, ma non registrano mai una poppata da soli. Sei tu a decidere cosa è successo."),
            ("Indicazioni con le fonti.", "Ogni numero viene da indicazioni sanitarie pubblicate, con il riferimento in vista. Indicative, mai prescrittive."),
            ("Pensata per due.", "Crescere un figlio si fa in due, e così l'app. Entrambi i telefoni vedono la stessa giornata, in tempo reale."),
        ],
        "pv_eyebrow": "Privacy",
        "pv_title": "Non vediamo mai i dati del tuo bambino.",
        "pv_lead": "Melian non ha account né server. Poppate, pannolini e crescita sono salvati sul tuo iPhone e nell'iCloud privato della tua famiglia, condivisi solo con il partner che inviti. Non possiamo leggerli, venderli o perderli.",
        "pv_link": "Leggi l'informativa sulla privacy",
        "dg_you": "Il tuo iPhone", "dg_cloud": "Il tuo iCloud", "dg_partner": "iPhone del partner", "dg_us": "Melian, lo sviluppatore", "dg_us_sub": "nessun accesso", "dg_private": "privato, cifrato da Apple",
        "quote": "Melian è nata alle 3 di notte, con una neonata, un biberon e un telefono pieno di appunti che non tornavano. Volevo qualcosa che fosse come una mano calma sulla spalla: dimmi quando ha mangiato l'ultima volta, ricordami quando avrà fame, e lasciami tornare a dormire.",
        "cite": "Marco, papà e autore di Melian",
        "end_title": "Presto sull'App Store.",
        "end_lead": "Melian è in prova con alcune famiglie. È per iPhone con iOS 26 o successivo, in italiano e in inglese.",
        "footer_note": "Melian mostra solo indicazioni orientative e non è un dispositivo medico.",
        "pp_title": "Informativa sulla privacy", "pp_meta": "Ultimo aggiornamento",
        "pp_summary": "<strong>Melian non raccoglie alcun dato personale.</strong> Tutto ciò che registri resta sui tuoi dispositivi e nel tuo account iCloud. Noi, lo sviluppatore, non possiamo vederlo.",
        "pp_body": """
<h2>Chi siamo</h2>
<p>Melian è realizzata da Marco Mattia Garoglio, sviluppatore indipendente in Italia (“noi”). Questa informativa riguarda l'app Melian per iPhone e i suoi widget.</p>
<h2>Cosa salva Melian, e dove</h2>
<p>Usando Melian puoi registrare nome, data di nascita, sesso, età gestazionale e una foto facoltativa del bambino, insieme a poppate, cambi di pannolino, note e misure di crescita, e il nome che scegli di mostrare sulle tue registrazioni.</p>
<ul>
<li><strong>Sul tuo iPhone.</strong> Queste informazioni sono salvate sul dispositivo, così l'app, i widget e la Live Activity possono mostrarle.</li>
<li><strong>Nel tuo iCloud.</strong> Se hai effettuato l'accesso a iCloud, Melian le sincronizza nel database privato del tuo account iCloud tramite CloudKit di Apple. Sono trattate da Apple secondo la <a href="https://www.apple.com/it/legal/privacy/">privacy policy di Apple</a>. Non abbiamo accesso ai tuoi dati iCloud privati.</li>
<li><strong>Con le persone che inviti.</strong> Se inviti il partner dalle Impostazioni, i dati sono condivisi con lui o lei tramite la condivisione iCloud. Puoi interrompere la condivisione in qualsiasi momento.</li>
<li><strong>Nei tuoi backup.</strong> Melian salva ogni giorno un file di backup in File › Sul mio iPhone › Melian. Questi file restano sul dispositivo, a meno che tu non li sposti o li condivida.</li>
</ul>
<h2>Cosa raccogliamo</h2>
<p>Niente. Melian non ha account, analisi statistiche, pubblicità, tracciamento né SDK di terze parti. Non vendiamo, non cediamo e non condividiamo dati, perché non li riceviamo mai.</p>
<p>Se nelle impostazioni di iOS hai scelto di condividere le analisi con gli sviluppatori, Apple può inviarci rapporti sugli arresti anomali e statistiche d'uso anonimi. Non contengono le informazioni che registri in Melian.</p>
<h2>Promemoria, sveglie e Siri</h2>
<p>Promemoria e sveglie delle poppate sono programmati sul tuo iPhone. Se usi Siri o Comandi con Melian, la richiesta è gestita da Apple.</p>
<h2>Minori</h2>
<p>Melian è usata da genitori e da chi si prende cura del bambino per registrare informazioni che lo riguardano. Non è rivolta ai bambini. Poiché non raccogliamo dati, nessuna informazione su alcun bambino arriva mai a noi.</p>
<h2>Le tue scelte</h2>
<ul>
<li>Per esportare i dati, usa Impostazioni › Esporta i dati nell'app.</li>
<li>Per cancellare tutto, elimina Melian dall'iPhone, poi rimuovi i suoi dati in Impostazioni di iOS › il tuo nome › iCloud › Gestisci spazio › Melian. Il partner mantiene l'accesso finché non interrompi la condivisione.</li>
</ul>
<p>Poiché non conserviamo dati personali che ti riguardano, non c'è nulla che dobbiamo consultare, correggere o cancellare per tuo conto. Restano comunque tutti i diritti previsti dal GDPR, e puoi contattarci per qualsiasi domanda.</p>
<h2>Modifiche</h2>
<p>Se questa informativa cambia, aggiorneremo questa pagina e la data qui sopra. Una modifica che iniziasse a raccogliere dati richiederebbe prima il tuo consenso nell'app.</p>
<h2>Contatti</h2>
<p>Domande sulla privacy? Vedi la <a href="support.html">pagina di assistenza</a>.</p>
""",
        "sp_title": "Assistenza", "sp_lead": "Domande, problemi o idee? Ogni messaggio è letto dalla persona che realizza Melian.",
        "sp_contact": "Scrivici",
        "sp_contact_note": "Apre un breve modulo su GitHub.",
        "faq_title": "Domande frequenti",
        "faq": [
            ("Come invito il partner?", "Apri Impostazioni › Invita il partner e invia l'invito con Messaggi, Mail o un'altra app. Il partner lo apre sul suo iPhone con Melian installata, e da quel momento i due telefoni mostrano gli stessi dati."),
            ("La sveglia non ha suonato. Cosa controllo?", "In Melian, verifica che in Impostazioni › Promemoria poppate siano attivi Ricordami la poppata e Sveglia forte. Poi controlla che sveglie e notifiche siano consentite per Melian nelle Impostazioni di iOS. Con Impostazioni › Prova la sveglia puoi sentirla subito."),
            ("Un promemoria registra una poppata da solo?", "No. Il promemoria ti avvisa soltanto. Una poppata viene registrata solo quando tu o il partner toccate Poppata, nell'app, su un widget o sulla Live Activity."),
            ("Dove sono i miei dati e come faccio un backup?", "Sul tuo iPhone e nel tuo iCloud. Melian salva anche un backup giornaliero in File › Sul mio iPhone › Melian, e Impostazioni › Esporta i dati ne crea uno quando vuoi."),
            ("Come cancello tutto?", "Elimina Melian, poi vai in Impostazioni di iOS › il tuo nome › iCloud › Gestisci spazio › Melian e cancella i suoi dati."),
            ("Le quantità di latte sono un consiglio medico?", "No. Sono intervalli indicativi tratti da indicazioni sanitarie pubblicate, mostrati con la loro fonte. Segui sempre l'ostetrica, il pediatra o il medico."),
            ("Quali iPhone sono supportati?", "Qualsiasi iPhone con iOS 26 o successivo."),
        ],
    },
}


def head(s, lang, base, page_title, desc, path):
    alt_base = "../" if lang == "it" else "it/"
    other = s["other_code"]
    en_url = SITE_URL + path
    it_url = SITE_URL + "it/" + path
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{page_title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#eef0ff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0d20" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{base}assets/favicon.png">
<link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="it" href="{it_url}">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE_URL}assets/icon-512.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<div class="ambient" aria-hidden="true"><i data-depth=".08"></i><i data-depth=".16"></i><i data-depth=".24"></i></div>
<div class="grain" aria-hidden="true"></div>
"""


def nav(s, lang, base, page, home):
    other = s["other_code"]
    other_href = (("../" if lang == "it" else "it/") + page) if page != "index.html" else ("../" if lang == "it" else "it/")
    return f"""<nav class="nav glass" aria-label="Melian">
  <a class="brand" href="{home}"><img src="{base}assets/favicon.png" alt="" width="26" height="26">Melian</a>
  <a class="link hide-sm" href="{home}#story">{s['nav_story']}</a>
  <a class="link hide-sm" href="{home}#philosophy">{s['nav_philosophy']}</a>
  <a class="link" href="privacy.html">{s['nav_privacy']}</a>
  <a class="link" href="support.html">{s['nav_support']}</a>
  <a class="link lang" href="{other_href}" hreflang="{other}" lang="{other}">{other.upper()}</a>
</nav>
"""


def footer(s, lang, base, home):
    other = s["other_code"]
    return f"""<footer class="site">
  <div class="wrap">
    <span>© 2026 Marco Mattia Garoglio · {s['footer_note']}</span>
    <nav>
      <a href="{home}">Melian</a>
      <a href="privacy.html">{s['nav_privacy']}</a>
      <a href="support.html">{s['nav_support']}</a>
      <a href="{'../' if lang == 'it' else 'it/'}" hreflang="{other}" lang="{other}">{s['other_lang']}</a>
    </nav>
  </div>
</footer>
"""


def badge(s):
    return f"""<span class="badge glass" role="img" aria-label="{s['badge_small']} {s['badge']}">{ICON['apple']}<span><small>{s['badge_small']}</small>{s['badge']}</span></span>"""


def phone(s, cls="", alarm=False, name=None, age=None):
    alarm_html = f"""
      <div class="alarm" aria-hidden="true">
        <div class="bell"><span class="waves"><i></i><i></i><i></i></span>{ICON['bell']}</div>
        <strong>{s['alarm_title']}</strong>
        <span>{s['alarm_sub']}</span>
        <div class="btns"><b>{s['snooze']}</b><b>{s['fed']}</b></div>
      </div>""" if alarm else ""
    mini = lambda k, label, color: f"""<div class="mini" data-k="{k}"><svg viewBox="0 0 36 36"><circle class="t" cx="18" cy="18" r="15"/><circle class="b" cx="18" cy="18" r="15" stroke="{color}"/></svg><strong>0</strong><span>{label}</span></div>"""
    return f"""<div class="phone {cls}" data-live>
    <div class="screen">
      <div class="island"><span class="ic">{ICON['bottle'].replace('<svg', '<svg width="12" height="12"')}</span><span class="t"></span></div>
      <div class="status"><span>9:41</span><span class="bars"><i></i></span></div>
      <div class="app">
        <header>
          <span class="round-btn" aria-hidden="true">{ICON['moon']}</span>
          <div class="who"><b>{name or s['phone_name']}</b><span>{age or s['phone_age']}</span></div>
          <span class="round-btn plus" aria-hidden="true">+</span>
        </header>
        <div class="ring">
          <svg viewBox="0 0 100 100" aria-hidden="true">
            <defs><linearGradient id="ringGrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9e8ce0"/><stop offset="1" stop-color="#738cf2"/></linearGradient></defs>
            <circle class="track" cx="50" cy="50" r="46" fill="none" stroke-width="5"/>
            <circle class="bar" cx="50" cy="50" r="46" fill="none" stroke-width="5"/>
          </svg>
          <div class="label"><small>{s['since']}</small><strong>1h 40m</strong><em></em></div>
        </div>
        <div class="minis">
          {mini('formula', s['formula'], '#738cf2')}{mini('feeds', s['feeds'], '#9e8ce0')}{mini('wet', s['wet'], '#54b3db')}{mini('dirty', s['dirty'], '#dba366')}
        </div>
        <div class="actions">
          <button class="act feed" data-kind="feed">{ICON['bottle']}<span>{s['feed']}</span><small>{s['repeat']}</small></button>
          <button class="act wet" data-kind="wet">{ICON['drop']}<span>{s['wet']}</span></button>
          <button class="act dirty" data-kind="dirty">{ICON['leaf']}<span>{s['dirty']}</span></button>
          <button class="act both" data-kind="both">{ICON['half']}<span>{s['both']}</span></button>
        </div>
        <div class="timeline"><h4>{s['timeline']}</h4><ul></ul></div>
      </div>{alarm_html}
    </div>
  </div>"""


def strings_script(s):
    js = {"next": s["next"], "feedRow": s["feed_row"], "wetRow": s["wet_row"], "dirtyRow": s["dirty_row"], "bothRow": s["both_row"]}
    return f"<script>window.MELIAN_STRINGS = {json.dumps(js, ensure_ascii=False)};</script>"


def landing(lang):
    s = STRINGS[lang]
    base = "../" if lang == "it" else ""
    home = "./"
    h1 = "".join(f'<span class="line"><span>{l}</span></span>' for l in s["h1"])
    chapters = "".join(f"""
          <article class="chapter{' on' if i == 0 else ''}">
            <span class="n">0{i + 1}</span>
            <h2>{t}</h2>
            <p class="lead">{p}</p>
          </article>""" for i, (t, p) in enumerate(s["chapters"]))
    principles = "".join(f'<li class="reveal" style="--i:{i % 3}"><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(s["principles"]))
    st = s["statement"]
    rows = "".join(f'<div class="row"><b>{w}</b> <span>{w}</span> <b>{w}</b> <span>{w}</span></div>' for w in st)
    diagram = f"""<svg class="diagram reveal" viewBox="0 0 440 360" role="img" aria-label="{s['pv_title']}">
        <path class="wire" d="M105 140 C 105 118, 150 126, 150 104"/>
        <path class="wire" d="M335 140 C 335 118, 290 126, 290 104"/>
        <path class="blocked" d="M220 104 L 220 260"/>
        <line class="x" x1="207" y1="222" x2="233" y2="248"/><line class="x" x1="233" y1="222" x2="207" y2="248"/>
        <g class="node"><rect x="110" y="20" width="220" height="84" rx="24"/><text x="220" y="57" text-anchor="middle">{s['dg_cloud']}</text><text class="sub" x="220" y="81" text-anchor="middle">{s['dg_private']}</text></g>
        <g class="node"><rect x="10" y="140" width="190" height="70" rx="24"/><text x="105" y="181" text-anchor="middle">{s['dg_you']}</text></g>
        <g class="node"><rect x="240" y="140" width="190" height="70" rx="24"/><text x="335" y="181" text-anchor="middle">{s['dg_partner']}</text></g>
        <g class="node" opacity=".7"><rect x="110" y="260" width="220" height="80" rx="24"/><text x="220" y="296" text-anchor="middle">{s['dg_us']}</text><text class="sub" x="220" y="320" text-anchor="middle">{s['dg_us_sub']}</text></g>
      </svg>"""
    sync = '<svg class="sync" viewBox="0 0 220 60" aria-hidden="true"><path d="M0 40 C 60 0, 160 0, 220 40"/></svg>'
    html = head(s, lang, base, s["title"], s["description"], "") + nav(s, lang, base, "index.html", home) + f"""
<main>
  <section class="hero" id="top">
    <div class="wrap">
      <div>
        <p class="eyebrow">{s['eyebrow']}</p>
        <h1>{h1}</h1>
        <p class="lead">{s['lead']}</p>
        <div class="cta">{badge(s)}<a class="ghost" href="#philosophy">{s['ghost']} ↓</a></div>
      </div>
      <div class="stage">
        <div class="stars" aria-hidden="true"></div>
        {phone(s, 'hero-phone')}
        <p class="sr">{s['try']}</p>
      </div>
    </div>
    <div class="scroll-hint" aria-hidden="true">{s['scroll']}<i></i></div>
  </section>

  <section class="story" id="story" data-step="1">
    <div class="pin">
      <div class="wrap">
        <div class="phones">
          {phone(s, 'main-phone', alarm=True)}
          {sync}
          {phone(s, 'partner', name=s['partner_name'], age=s['partner_age'])}
        </div>
        <div>
          <div class="chapters">{chapters}
          </div>
          <div class="progress" aria-hidden="true">{''.join('<i></i>' for _ in s['chapters'])}</div>
        </div>
      </div>
    </div>
  </section>

  <section class="statement" aria-label="{' '.join(st)}">{rows}</section>

  <section class="principles" id="philosophy">
    <div class="wrap">
      <header class="reveal">
        <p class="eyebrow">{s['ph_eyebrow']}</p>
        <h2>{s['ph_title']}</h2>
        <p class="lead">{s['ph_lead']}</p>
      </header>
      <ol class="plist">{principles}</ol>
    </div>
  </section>

  <section class="privacy-band" id="privacy">
    <div class="wrap">
      <div class="reveal">
        <p class="eyebrow">{s['pv_eyebrow']}</p>
        <h2>{s['pv_title']}</h2>
        <p class="lead">{s['pv_lead']}</p>
        <a class="ghost" href="privacy.html">{s['pv_link']} →</a>
      </div>
      {diagram}
    </div>
  </section>

  <section class="note">
    <div class="wrap">
      <blockquote>{s['quote']}</blockquote>
      <cite>{s['cite']}</cite>
    </div>
  </section>

  <section class="end">
    <div class="wrap reveal">
      <img class="icon" src="{base}assets/icon-512.png" alt="Melian" width="112" height="112">
      <h2>{s['end_title']}</h2>
      <p class="lead">{s['end_lead']}</p>
      {badge(s)}
    </div>
  </section>
</main>
""" + footer(s, lang, base, home) + strings_script(s) + f'\n<script src="{base}assets/main.js" defer></script>\n</body>\n</html>\n'
    return html


def doc_page(lang, kind):
    s = STRINGS[lang]
    base = "../" if lang == "it" else ""
    home = "./"
    if kind == "privacy":
        title = s["pp_title"]
        body = f"""
    <p class="eyebrow">Melian</p>
    <h1>{title}</h1>
    <p class="meta">{s['pp_meta']}: {UPDATED[lang]}</p>
    <div class="summary glass"><p>{s['pp_summary']}</p></div>
    {s['pp_body']}"""
        desc = s["pp_summary"].replace("<strong>", "").replace("</strong>", "")
        path = "privacy.html"
    else:
        title = s["sp_title"]
        faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in s["faq"])
        body = f"""
    <p class="eyebrow">Melian</p>
    <h1>{title}</h1>
    <p class="lead">{s['sp_lead']}</p>
    <a class="badge glass contact" href="{CONTACT_URL}" rel="noopener">{ICON['bell'].replace('<svg', '<svg aria-hidden="true"')}<span><small>{s['sp_contact_note']}</small>{s['sp_contact']}</span></a>
    <h2>{s['faq_title']}</h2>
    {faq}"""
        desc = s["sp_lead"]
        path = "support.html"
    return head(s, lang, base, f"{title} · Melian", desc, path) + nav(s, lang, base, path, home) + f"""
<main class="doc">
  <div class="wrap">{body}
  </div>
</main>
""" + footer(s, lang, base, home) + f'<script src="{base}assets/main.js" defer></script>\n</body>\n</html>\n'


def main():
    for lang in ("en", "it"):
        out = ROOT if lang == "en" else ROOT / "it"
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(landing(lang), encoding="utf-8")
        (out / "privacy.html").write_text(doc_page(lang, "privacy"), encoding="utf-8")
        (out / "support.html").write_text(doc_page(lang, "support"), encoding="utf-8")
    print("built en + it")


if __name__ == "__main__":
    main()
