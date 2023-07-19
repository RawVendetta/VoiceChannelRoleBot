import discord

# Variables
BOT_TOKEN = ""
SERVER_NAME = ""
RULES_CHANNEL = ""  # Replace with the name of the rules channel
ROLE_NAME = ""  # Replace with the name of the specified role
DM_CONTENT = ""  # The message to be sent in the DM

intents = discord.Intents.default()
intents.reactions = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    target_guild = discord.utils.get(client.guilds, name=SERVER_NAME)
    if target_guild is not None:
        print(f"Bot is connected to the target server (guild): {target_guild.name}")
    else:
        print(f"Bot is not connected to the target server (guild): {SERVER_NAME}")

@client.event
async def on_voice_state_update(member, before, after):
    target_guild = discord.utils.get(client.guilds, name=SERVER_NAME)
    if target_guild is not None and before.channel is None and after.channel is not None:
        # Check if the user has the specified role
        role = discord.utils.get(target_guild.roles, name=ROLE_NAME)
        if role is not None and role not in member.roles:
            # Send DM to the user
            try:
                await member.send(DM_CONTENT)
                print(f"Rules Solicitation DM sent to {member.name}")
            except discord.Forbidden:
                print(f"Failed to send DM to {member.name}. The user might have DMs disabled.")

@client.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is in the specified rules channel
    channel_id = payload.channel_id
    target_guild = discord.utils.get(client.guilds, name=SERVER_NAME)
    if channel_id == target_guild.get_channel(payload.channel_id).id:
        user_id = payload.user_id
        # Get the member object from the user ID
        member = target_guild.get_member(user_id)
        # Check if the user has the specified role
        role = discord.utils.get(target_guild.roles, name=ROLE_NAME)
        if role is not None and role not in member.roles:
            # Assign the role to the user
            try:
                await member.add_roles(role)
                print(f"Assigned {ROLE_NAME} role to {member.name}")
            except discord.Forbidden:
                print(f"\nAttempted role assignment: {ROLE_NAME} --> {member.name}")
                print("[INFO    ] ChatterSync cannot assign roles to a member with higher permissions than itself.\n")

client.run(BOT_TOKEN)
