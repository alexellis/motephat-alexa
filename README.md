# Alexa skill for mote-phat by Pimoroni

## Control Pimoroni's home-lighting kit through Alex Skills kit with a Raspberry Pi

This Alexa skill provides utterances for changing the colour of our LEDs like "Alexa, ask mote change to blue" and will let us turn them off by saying "Alexa, tell mote turn off".

> This is an abridged version of a 2-page tutorial commissioned by Linux User and Developer Magazine. For the full experience subscribe to the publication or electronic PDF at https://linuxuser.co.uk/

![Mote](https://cdn.shopify.com/s/files/1/0174/1800/products/mote-6_1_large.jpg?v=1473845101)

## Resources:

* [mote-phat](https://shop.pimoroni.com/products/mote-phat) product page
* [mote-phat/examples](https://github.com/pimoroni/mote-phat/tree/master/examples) on Github

## Instructions

* Prepare your Raspberry Pi and mote

Solder a male 40-pin header to your Pi Zero or if you have a regular Pi skip this step.

Now solder the 40-pin female header to your mote-phat.

* Flash the base system

Flash a new SD card with Raspbian Jessie Lite making sure to create a file in the boot partition called `ssh` this will let us connect over SSH remotely and copy/paste commands without needing UI packages or a screen. Once plugged in your Pi will be accessible via `ssh pi@raspberrypi.local`.

* Setup ngrok

Download and unzip ngrok for Linux ARM into `/usr/bin` https://ngrok.com/download

* Install Docker

Docker is a packaging and runtime system that allows us to build, ship and run software easily. I've used it in this tutorial so that you don't have to manually configure your Raspberry Pi with the libraries and runtimes needed for the project. If you want to bypass Docker then check out the [Dockerfile](https://github.com/alexellis/motephat-alexa/blob/master/Dockerfile) and run the steps in manually with bash.

Run these two commands, then logout and log in again. This is so that the `pi` user's access to Docker can be refreshed.

```
# curl -sSL get.docker.com | sh
# sudo usermod pi -aG docker
```

You can read the contents of the [Dockerfile here](https://github.com/alexellis/motephat-alexa/blob/master/Dockerfile).

Now clone the Github repository and build the Docker image (this will take some time):

```
# apt-get update && apt-get -qy install git
# git clone https://github.com/alexellis/motephat-alexa
# docker build -t alexamote .
```

The resulting Docker image contains everything needed for our application in an isolated package. Read the `Dockerfile` if you want to know more.

* Run the code

Our project's code is packaged with all its dependencies into a single container. We can now run that in the background and open the ngrok HTTPs tunnel to the internet. The flag `-p` tells Docker to expose the port for our web-server code that talks to Alexa. The `-d` flag tells the service to run in the background.

```
# docker run --name mote --privileged -d -p 5000:5000 alexamote
# ngrok http 5000 > /dev/null &
# curl localhost:4040/api/tunnels | jq -r ".tunnels[1].public_url "
```

Take note of your `public_url` beginning with https. This changes every time the ngrok process starts.

If you want to stop the mote-phat process later on you can type in `docker rm -f mote` or `docker ps` to view its status.

* Test the endpoint

Once you have your HTTPs URL from `ngrok` then you can test everything out by sending in a request just like the one the Alexa SDK creates. We have captured two samples and saved them in the Git repository.

Test going red:

```
# curl -X POST -H "Content-type: application/json" -d @coloursample.json https://c00738f6.ngrok.io
```

Test turning the lights off:

```
# curl -X POST -H "Content-type: application/json" -d @offsample.json https://c00738f6.ngrok.io
```

> Make sure you replace the HTTPs URL with your URL from ngrok.

* Create an Alexa skill

Head over to https://developer.amazon.com/myapps.html and click Alexa -> Alexa Skills Kit -> Get Started. You may need to register for this step and provide billing information for any purchases you want to make.

Click "Add a New Skill" -> "English UK" and type in "mote" for the "Name" and "Invocation Name" fields. For the "Intent Schema" copy/paste `speechAsssets/intentSchema.json` and for Sample Utterances `speechAsssets/sampleUtterances.txt`. You must also add a Custom Slot called Colour with the values: red/green/blue on separate lines. The custom slot helps Alexa by providing a list of all the things you could say to her - it's like a parameter in coding.

* Point Alexa to your HTTPs endpoint

Under the "Configuration" tab of your Alexa Skill click "Service Endpoint Type: HTTPs". Then select "Europe" as the nearest region and paste in the ngrok URL from earlier.

Now click "My development endpoint has a certificate from a trusted certificate authority" on the "SSL Certificate" tab.

On the "Test" tab you can type in sample utterances such as "change to blue" or "turn off" - when you click "Ask mote" a message will be transmitted to your Pi from Alexa's online service bypassing the Echo/dot.

* Talk to your Echo

If everything worked you will be able to talk to your Echo/dot. Simply say "Alexa, ask mote change to red" or "Alexa, ask mote to turn off".

* Take it further

Now that you have created your first skill maybe you can think of some ways to extend it or to apply it to other hardware projects?

We think dimming the light could be useful and it should be easy to add other colours. If you want to know more about Docker check out the box-out, the included Dockerfile and Alex's beginner tutorials at: http://blog.alexellis.io/tag/raspberry-pi/

If you have questions, comments or suggestions please get in touch on Twitter [@alexellisuk](https://twitter.com/@alexellisuk).

**Add new utterances**

You can create other ways of invoking the code by editing speechAsssets/sampleUtterances.txt

**Extending the skill's code**

The skill is written in Python so you will need to change app.py and/or mote.py.

To implement an optional brightness level you could take inspiration from my Christmas Tree hack's source-code: http://blog.alexellis.io/christmas-iot-tree/

**Create a web test page**

You could also create a test-page for the device, this could be useful if you do not have an Alexa device yet or want to control the lights from another room. The code is written in Python with the Flask library providing a web-server and HTML templating. My pyPlaylist project gives an example of serving up a small Angular app: https://github.com/alexellis/pyPlaylist/
