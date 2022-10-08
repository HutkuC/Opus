from pytube import YouTube


class Download:

    @staticmethod
    def download(ctx, url):

        yt = YouTube(url=url)
        video = yt.streams.filter(only_audio=True).first()
        destination = 'sound_files'
        video.download(output_path=destination, filename=str(ctx.guild.id) + '.mp3')
        print(yt.title + " has been successfully downloaded as " + str(ctx.guild.id) + ".mp3")
