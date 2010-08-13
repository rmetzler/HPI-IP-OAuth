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

## OAuth 

OAuth is an open protocol to allow secure API authorization in a simple and standard method from desktop and web applications.

It enables __users__ to authenticate and authorize 3rd party applications called __OAuth consumers__ to access data that is associated with a __resource__ managed by the __service provider__.

![OAuth parties](HPI-IP-OAuth/raw/master/OAuth.png) [OAuth parties image](HPI-IP-OAuth/raw/master/OAuth.png)

## OAuth Example Service



## Implementing OAuth in HPIIP

### Web-Layer

### Persistence-Layer

### API-Layer

[Talk: OpenID vs OAuth](http://www.slideshare.net/rmetzler/identity-on-the-web-openid-vs-oauth)





