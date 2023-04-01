import discord
import config
###REGELN###

offi_Regeln = discord.Embed(
    title="Serverregeln",
    color=config.KEKS_ORANGE,
)
offi_Regeln.add_field(
    name="§1 Allgemein", 
    value="""§1.1 Den Ownern steht das Recht zu, die Regeln nach Belieben zu erweitern oder anzupassen.
§1.2 Mit dem Betreten des Discord Servers akzeptierst du diese Regeln und verpflichtest dich, diese zu befolgen.
§1.3 Bei Nicht-Befolgung dieser Regeln hat das Wolkenlos Team das Recht, Strafen aussprechen.
§1.4 Hört auf die Moderatoren und Administratoren.
§1.5 Die Regeln gelten zum Teil nicht für Moderatoren und Administratoren.
""", inline=False
)

offi_Regeln.add_field(
    name="§2 Chatregeln",
    value="""§2.1 Jegliche Beleidigungen, Anfeindungen und Drohungen an den Server oder sonstige Beteiligte sind verboten.
§2.2 Das wiederholte Schreiben vom gleichem oder ähnlichem Wortlaut innerhalb kurzer Zeitspanne nennt sich Spam und ist verboten.
 Unter Spam versteht sich das Senden mehrerer gleichbedeutender Nachrichten innerhalb einer Minute.
 Die gleichen oder ähnlichen Nachrichten von mehreren Personen innerhalb einer Minute werden auch als Spam gezählt.
§2.3 Keine unerlaubten Links und keine unerlaubte Werbung in den normalen Chats.
§2.4 Radikalismus in jeglicher Form ist strengstens untersagt.
§2.5 Rassismus und fremdenfeindliche Äußerungen in jeglicher Form sind strengstens verboten.
§2.6 Sich als eine andere Person auszugeben ist verboten.
§2.7 Nicht mit Caps schreiben. Dies kann zu einem unverzüglichen Kick oder Bann führen.
§2.8 NSFW- und obszöne Inhalte werden nicht geduldet.
§2.9 Die Chatregeln gelten sowohl für den Discord Server, als auch für den Minecraft Server."""
, inline=False
)

#file = discord.File("Bilder\Wolkenlos.png", filename="Wolkenlos1.png")

#offi_Regeln.set_author(name="Wolkenlos Team", icon_url="attachment://Wolkenlos1.png")


