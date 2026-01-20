import discord
from discord.ext import commands, tasks
import discord.ext.commands
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid

class MoneySplitCrud(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name='create_moneysplit', help='Creates a new moneysplit transaction. Usage: !create_moneysplit @person1 @person2')
    async def create_moneysplit(self, ctx, *, args=None):
        try:
            # Generate unique UUID for this money split transaction
            transaction_id = str(uuid.uuid4())
            
            # Get the author's ID
            author_id = str(ctx.author.id)
            
            # Parse mentioned users
            participants = [author_id]  # Add the creator
            
            if ctx.message.mentions:
                for mention in ctx.message.mentions:
                    if mention.id != ctx.author.id:  # Don't add the author twice
                        participants.append(str(mention.id))

            moneysplit_ref = self.db.reference('moneysplit')
            if not moneysplit_ref.get():
                moneysplit_ref.set({})

            # Create the moneysplit entry in Firebase
            ref = self.db.reference(f'moneysplit/{transaction_id}')
            ref.set({
                'creator': author_id,
                'participants': participants,
                'created_at': int(ctx.message.created_at.timestamp()),
                'transactions': {}
            })
            
            participant_names = ", ".join([f"<@{p}>" for p in participants])
            embed = discord.Embed(
                title="moneysplit Created!",
                description=f"**ID:** `{transaction_id}`\n**Participants:** {participant_names}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            embed = discord.Embed(
                title=":warning: Error creating moneysplit",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

    @commands.command(name='add_moneysplit', help='Adds a user to an existing moneysplit transaction. Usage: !add_moneysplit <transaction_id> @person')
    async def add_moneysplit(self, ctx, transaction_id: str, *, args=None):
        if not ctx.message.mentions:
            raise commands.BadArgument("You must mention at least one person to add!")
        
        ref = self.db.reference(f'moneysplit/{transaction_id}')
        moneysplit_data = ref.get()
        
        if not moneysplit_data:
            raise commands.BadArgument(f"moneysplit transaction `{transaction_id}` not found!")
        
        # Get current participants
        participants = moneysplit_data.get('participants', [])
        
        # Add new participants
        added_users = []
        for mention in ctx.message.mentions:
            user_id = str(mention.id)
            if user_id not in participants:
                participants.append(user_id)
                added_users.append(mention.mention)
        
        # Update the database
        ref.update({'participants': participants})
        
        embed = discord.Embed(
            title="User(s) Added!",
            description=f"Added {', '.join(added_users)} to moneysplit `{transaction_id}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)



    @add_moneysplit.error
    async def add_moneysplit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title=":warning: Invalid input for !add_moneysplit",
                description="You must provide a transaction ID! Usage: !add_moneysplit <transaction_id> @person",
                color=discord.Color.red()
            )
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title=":warning: Invalid input for !add_moneysplit",
                description=str(error),
                color=discord.Color.red()
            )
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=":warning: Error adding user to moneysplit",
                description=str(e),
                color=discord.Color.red()
            )
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)