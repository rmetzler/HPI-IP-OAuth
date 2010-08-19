Integrating OAuth Protocol in HPI Identity Provider
===================================================

_Abstract:_ People using very many different internet services today. It is hard for users to remember all these different usernames and passwords so they often use the same username and password on different sites. This is a security issue that protocols like OpenID an OAuth try to solve. By creating a single online identity and allowing 3rd party sites to authenticate users an identity provider is able to solve the security issue and enable single sign-on (SSO) above different websites.

_Keywords:_ OAuth, SSO, online identity, identity provider, API security

_Author:_ Richard Metzler


##Table of Contents
- Introduction
- The OAuth Protocol
- OAuth Example Service
- Implementing OAuth in HPIIP


## Introduction

Every day people use many different internet websites for their online activities. While some of these websites are used by only a few to several thousend people, some other websites like webbased email programms or social networking websites are visited by millions of users on a daily basis. Google's GMail, Facebook and Twitter are aiming to become the center of our online activities and therefor the provider of our online identity. One way to achieve this is to enable 3rd party sites to allow users to sign up with accounts from these sites. This is possible through protocols like OpenID and OAuth that are able to authenticate a user and redirect him back to the 3rd party website.

For users this feature enables a more secure and better online experience as they are not required to register  with username and password at every website they want to try out. For the third party service this often means that their sign-up conversion rate can dramatically increase.

In this paper we describe the OAuth 1.0a protocol. Then we describe our proposed privacy service that is granted access to the HPI identity provider via OAuth. We explain the changes we made in order to enable OAuth in the HPI-IP and how the API works.

## The OAuth Protocol 

__OAuth__ is an open protocol to allow secure API authorization in a simple and standard method from desktop and web applications. [OAuth-spec] It enables __users__ to authenticate and authorize 3rd party applications called __OAuth consumers__ to access data that is associated with a __resource__ managed by the __service provider__.

![OAuth parties](HPI-IP-OAuth/raw/master/OAuth.png)  
The three different parties in OAuth protocol.

In order to authenticate an user and enabling authorization an OAuth consumer has to be registered at the service provider. Through registration the service provider obtains a dedicated consumer key & secret pair that is used for authenticating the service whenever user access is requested. 

### OAuth Dance

When a user wants to authenticate a webservice via OAuth the __OAuth authentication flow__ (commonly referred to as OAuth dance) is executed.
 
The following description is very simplified as details that are important for securing this flow and preventing from replay attacks like the _signature method_ and the _nonce_ are missing from it. The description is first and foremost meant to provide a general understanding of the OAuth authentication flow as an exact description is beyond the scope of this paper.

The authentication flow is started by the user clicking on a special link on the website of the OAuth consumer. The consumer uses his consumer key and secret to request a __unauthorized OAuth request token__ and __secret__ from the service provider. This OAuth token is used to identify the authentication context for the user.

After obtaining the request token, the user is redirected from the consumer to the service provider. Thereby the request token is appended on the URL. The user is authenticated and can now authorize the consumer. The service provider directs the user back to the consumer.

When the user returns to the consumer the consumer uses the request token to request an __access token__ & secret from the service provider. The service provider exchanges the request token for the access token thereby granting access to the user's resource(s) as long as the token is valid.


![OAuth dance](http://a0.twimg.com/images/dev/oauth_diagram.png)  
source: [http://dev.twitter.com/pages/auth](http://dev.twitter.com/pages/auth)

## OAuth Privacy EMail Service for HPIIP

One main feature of the HPIIP is to act as an __identity provider__ and issue __IdentityCards__. These Identity Cards can be used by the user to sign up to a __relying party__. Then the relying party requests the associated attribute values from the identity provider. This could be something like the name, home address or the email address of the user. 

In order to verify email addresses of new signed up users services often send an email with an authentication link. The user has to click this link to verify that this is an valid email address and the user actually owns it.

Often an user only wants to try out a new service but don't want to provide his real email address in fear of SPAM from the service. Our proposed OAuth example service should be able to change the associated email address value of an identity card when it is authorized by the user.

To grant access to the identity card the user authorize the Privacy EMail Service by clicking on a "Log in to HPI IP" button on the Privacy EMail Service site. The service then acts as a OAuth consumer, redirecting the user's browser to the HPI IP website to login. The user then can grant access of the identity cards to the consumer.

The service changes the value of the email address in an issued identity card every 10 minutes to a temporary valid email address the service has control of. Whenever a user uses the identity card to sign up to a relying party, the relying party asks the identity provider for the current email address and sends an email. Because the OAuth service forwards emails for 20 minutes to the actual email address of the user and ignores emails to the temporary address received thereafter the user will receive only the emails from the relying party that are send in this short time window. All emails received later are considered 'SPAM' and will be ignored. 

Below is a sequence diagram of the described behaviour.
![OAuth Example Service Sequence](HPI-IP-OAuth/raw/master/example-service-seq.png)  

## Implementing OAuth in HPI IP

OAuth defines three request endpoint URLs:
+ Request Token URL - we use _/oauth/request\_token_
+ User Authorization URL - we use _/oauth/authorize_
+ Access Token URL - we use _/oauth/access\_token_

We need to implement everyone of these of these endpoints with the Tapestry web framework used by HPI IP.

### Request Token URL

When the consumer sends an HTTP requests to the Request Token URL _/oauth/request\_token_ there must be the following parameters specified:

+ _realm_
+ _oauth\_consumer\_key_
+ _oauth\_signature\_method_
+ _oauth\_callback_
+ _oauth\_signature_

The service provider must validate the incoming OAuth message and verify the consumer by checking his credentials against the database. Then the service provider creates a new set of temporary credentials and returns it in a HTTP response body using  _"application/x-www-form-urlencoded"_ content type.

If the request was valid the response contains the following url encoded parameters:

+ _oauth\_token_
+ _oauth\_token\_secret_
+ _oauth\_callback\_confirmed_

This oauth token is called the _request token_ and it is used to identify the OAuth authorization flow. 

### User Authorization URL

After receiving the _request token_ the OAuth consumer redirects the user's web browser to the _authorization url_. The request token must be appended as parameter __oauth\_token__ to the authorization url. 

The provider has to verify the identiy of the user and then ask to authorize the requested access. Therefor the OAuth provider should display informations about the client (like name, url or logo) based on the request token for the user to verify.  

The provider has to delete or mark the request token as used to prevent repeated authorization attempts. If the user authorize the consumer that the user's webbrowser is redirected to the cpnsumer's callback url and _oauth\_token_ and _oauth\_verifier_ are appended as parameters.


### Access Token URL

When the user is redirected to the OAuth consumer the consumer uses the _oauth\_verifier_ to obtain the permanen access token. To do this the _oauth\_verifier_ is added to the list of parameters the consumer used to obtain the request token and all parameters are appended to the access token url.

The server must verify the validity of the request. Ig the request is valid and authorized the permanent token credentials are includes as "application/x-www-form-urlencoded" content type with status code 200 (OK) in the HTTP response. The parameters are

+ _oauth\_token_
+ _oauth\_token\_secret_

Once the client receives and stores the token credentials it can use it to access protected resorces on behalf of the resource owner. To do so the consumer has to use his credentials together with the access token credentials received.

### Making Requests

Whenever the consumer tries to access the user's restricted resource he has to add the OAuth protocol parameters to the request by using the OAuth HTTP "Authorization" header field. The required parameters are:

+ _oauth\_consumer\_key_
+ _oauth\_token_
+ _oauth\_signature\_method_
+ _oauth\_timestamp_
+ _oauth\_nonce_
+ _oauth\_signature_

The server has to validate the authenticated request by recalculating the request signature, ensuring that the combination of nonce/timestamp/token has never used before and verify that the scope and status of the authorization as represented by the token is valid. 

### Web-Layer

### Persistence-Layer

### API-Layer

## Implementing OAuth Privacy Service

Our example service has to be a webservice able to receive and send emails. Because we were not in control of and did not want to set up an own SMTP server we choose to use [Google AppEngine].

Google AppEngine is a _Plattform as a Service_ infrastructure framework provided by Google. Developers can use Python and Java to programm web application on top of this infrastructure. Like most web frameworks AppEngine also implements the Model-View-Controller pattern. The framework also has APIs to receive and send emails and start Cron jobs.

Our Model needs to save OAuth tokens to the database that are associated with the real email address and the temporary valid email address. This is what our modelclass ... in ... .py does.


## Sources


[OAuth-spec]

[Talk: OpenID vs OAuth](http://www.slideshare.net/rmetzler/identity-on-the-web-openid-vs-oauth)

__TODO: link to 2nd talk__

[RFC]: http://tools.ietf.org/html/rfc5849 "RFC 5849"
[OAuth-spec]: http://oauth.net/ "OAuth specification"
[Google AppEngine]: "http://appengine.google.com" "Google AppEngine"
