import discord
from discord.ext import commands
from model import get_class
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='*', intents=intents)

@bot.event
async def on_ready():
    print(f'🤖EcoVision Bot has logged in as {bot.user}')
    channel_id = 1441730537260712006
    channel = bot.get_channel(channel_id)

    if channel:
        await channel.send("🤖EcoVision Bot has logged in, use *help to see the commands!")
    else:
        print("Channel tidak ditemukan!")


@bot.command()
async def hello(ctx):
    """Menyapa pengguna"""
    await ctx.send(f'Hi👋! I am {bot.user}!')

# --- Perintah utama: deteksi gambar ---
@bot.command()
async def check(ctx):
    """Deteksi gambar yang dikirim pengguna"""
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            # Simpan gambar sementara
            file_name = attachment.filename
            save_path = f"./{file_name}"
            await attachment.save(save_path)

            await ctx.send(f"🖼️ Gambar berhasil disimpan: `{file_name}`")

            try:
                # Jalankan fungsi deteksi dari model.py
                hasil = get_class(
                    model_path="./keras_model.h5",
                    labels_path="./labels.txt",
                    image_path=save_path
                )
                await ctx.send(f"♻️ Hasil deteksi: **{hasil}**")
                print(hasil)
                # Tips tambahan sesuai kategori
                tips = {
                    "plastik": "Cuci bersih dan kirim ke bank sampah ♻️",
                    "kertas": "Gunakan kembali atau daur ulang 📄",
                    "logam": "Bisa dijual ke pengepul logam 💰",
                    "organik": "Cocok dijadikan kompos alami 🌱"
                }

                kategori = hasil.split("(")[0].strip().lower()
                if kategori in tips:
                    await ctx.send(f"💡 Tips: {tips[kategori]}")
                else:
                    await ctx.send("💡 Tips: Pisahkan sampah agar mudah dikelola kembali 🌍")

            except Exception as e:
                await ctx.send(f"⚠️ Terjadi kesalahan saat memproses gambar: {e}")

            # Hapus gambar sementara setelah digunakan
            if os.path.exists(save_path):
                os.remove(save_path)
    else:
        await ctx.send("📷 Anda lupa mengirim gambar. Gunakan perintah `*check` dan unggah gambar setelahnya.")

# --- Perintah tambahan: announce ---
@bot.command()
async def announce(ctx, *, message: str):
    """Mengumumkan pesan di channel saat ini"""
    await ctx.send(f"📢 {message}")

bot.run("")