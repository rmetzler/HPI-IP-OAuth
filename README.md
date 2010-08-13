Integrating OAuth protocol in HPI Identity Provider
===================================================

_Abstract:_ People using very many different internet services today. It is hard for users to remember all these different usernames and passwords so they often use the same username and password on different sites. This is a security issue that protocols like OpenID an OAuth try to solve. By creating a single online identity and allowing 3rd party sites to authenticate users an identity provider is able to solve the security issue and enable single sign-on (SSO) above different websites.

_Keywords:_ OAuth, SSO, online identity, identity provider, API security

_Author:_ Richard Metzler


##Table of Contents
- Introduction
- OAuth
- OAuth Example Service
- Implementing OAuth in HPIIP


## Introduction

Every day people use many different internet websites for their online activities. While some of these websites are used by only a few to several thousend people, some other websites like webbased email programms or social networking websites are visited by millions of users on a daily basis. Google's GMail, Facebook and Twitter are aiming to become the center of our online activities. One way to achieve this is to enable 3rd party sites to allow users to sign up with accounts from these sites. This is possible through protocols like OpenID and OAuth that are able to authenticate a user and redirect him back to the 3rd party website.

For users this often enables a more secure and better online experience as they are not required to register with username and password. For the third party service this often means that their sign-up conversion rate can dramatically increase.



In this paper we describe the OAuth 1.0a protocol. Then we describe our  proposed privacy service that is granted access to the HPI identity provider via OAuth. We explain the changes we made in order to enable OAuth in the HPIIP and how the API works.

## OAuth 

__OAuth__ is an open protocol to allow secure API authorization in a simple and standard method from desktop and web applications. It enables __users__ to authenticate and authorize 3rd party applications called __OAuth consumers__ to access data that is associated with a __resource__ managed by the __service provider__.

![OAuth parties](HPI-IP-OAuth/raw/master/OAuth.png)  
The three different parties in OAuth protocol.

In order to authenticate an user and enabling authorization an OAuth consumer has to be registered at the service provider. Through registration the service provider gets a dedicated consumer key & secret pair that is used for authenticating the service whenever user access is requested. 

### OAuth Dance

When a user wants to authenticate a webservice via OAuth the __OAuth authentication flow__ (commonly referred to as OAuth dance) is executed.
 
The following description is very simplified as details that are important for securing this flow and preventing from replay attacks like the _signature method_ and the _nonce_ are missing from it. The description is first and foremost meant to provide a general understanding of the OAuth authentication flow as an exact description is beyond the scope of the paper.

The authentication flow is started by the user clicking on a special link on the website of the OAuth consumer. The consumer uses his consumer key and secret to request a __unauthorized OAuth request token__ and __secret__ from the service provider. This OAuth token is used to identify the authentication context for the user.

After obtaining the request token, the user is redirected from the consumer to the service provider. Thereby the request token is appended on the URL. The user is authenticated and can now authorize the consumer. The service provider directs the user back to the consumer.

When the user returns to the consumer the consumer uses the request token to request an __access token__ & secret from the service provider. The service provider exchanges the request token for the access token thereby granting access to the user's resource(s) as long as the token is valid.


![OAuth dance](http://a0.twimg.com/images/dev/oauth_diagram.png)  
source: [http://dev.twitter.com/pages/auth](http://dev.twitter.com/pages/auth)

## OAuth Privacy Service for HPIIP

One main feature of the HPIIP is to act as an __identity provider__ and issue __IdentityCards__. These Identity Cards can be used by the user to sign up to a __relying party__. Then the relying party requests the associated attribute values from the identity provider. This could be something like the name or the address of the user. 

In order to verify email addresses of new signed up users services often send an email with an authentication link. The user has to click this link to verify that this is an valid email address and the user actually owns it.

Often an user only wants to try out a new service but don't want to provide his real email address in fear of SPAM from the service. Our proposed OAuth example service should be able to change the associated email address value of an identity card when it is authorized by the user.

The service changes the value of the email address in an issued identy card every 10 minutes. Whenever a user uses the identity card to sign up to a relying party, the relying party asks the identity provider for the current email address and sends an email. Because the OAuth service forwards emails for 20min to the actual email address of the user and ignores emails send after this the user will receive only the emails from the relying party that are send in this short time window. All emails after this are considered 'SPAM' and ignored. 

This is a sequence diagram of the described behaviour.
![OAuth Example Service Sequence](HPI-IP-OAuth/raw/master/example-service-seq.png)  


## Implementing OAuth in HPIIP

### Web-Layer

### Persistence-Layer

### API-Layer

[Talk: OpenID vs OAuth](http://www.slideshare.net/rmetzler/identity-on-the-web-openid-vs-oauth)





