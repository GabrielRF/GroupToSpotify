# Group to Spotify Telegram bot

http://telegram.me/SpotifyRobot_bot

Bot que captura todas as músicas do Spotify compartilhadas via link em um grupo e as coloca em uma playlist.

![GroupToSpotify](http://i.imgur.com/Gw43LAZ.png)

===

## Configuração

Clone ou baixe o repositório e instale os requisitos

```
pip install -r requirements.txt
```

Crie um arquivo de configuração e faça os ajustes devidos

```
cp bot.conf_sample bot.conf
```

`TOKEN` = Token do bot, gerado pelo [@BotFather](http://telegram.me/botfather)

`CHANNEL_GROUP_ID` = ID do grupo em que o bot capturará as músicas

`CLIENT_ID` = ID de cliente do Spotify

`CLIENT_SECRET` = Chave secreta de cliente do Spotify

`REDIR_URI` = URL que receberá a autorização de uso do novo app para Spotify

`SIZE` = Tamanho do histórico

`USER_ID` = ID de Usuário do Spotify

`PLAYLIST_ID` = ID da playlist

`WRITE` = Retorno do bot além do retorno no próprio grupo

## Funcionamento

Para que o bot comece a funcionar,

```
python gtc.py
```

No primeiro uso o bot irá gerar uma URL para autorizar o bot a acessar seu Spotify. Siga os passos e tudo deverá ocorrer normalmente. Esta autorização é necessária ser feita somente uma vez.

## Contribua

Todo pull-request é extremamente bem-vindo!

## To-do

[Ver issues](https://github.com/GabrielRF/GroupToSpotify/issues)

Basicamente o que falta fazer é:

##### Utilizar um banco de dados em vez de um arquivo de configuração para os dados dos grupos

Isto irá facilitar o uso do bot em outros grupos. Atualmente a configuração é manual. Quero automatizar tudo.

##### Permitir autorização via Telegram, sem necessitar interação com o Terminal

Imagino o bot sendo adicionado à um grupo e retornando uma URL. O dono da playlist clica na URL e autoriza o bot. A URL de retorno então entrega o `code` ao bot usando deeplink, permitindo o bot acessar o Spotify e não necessitando mais de intervenções via Terminal.
