<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LIANCP — System Showcase</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#030303;--text:#f0ede6;--dim:#706f6a;--accent:#c4a35a;--accent2:#e6c99e;--surface:rgba(255,255,255,0.03);--border:rgba(255,255,255,0.06)}
html{font-size:16px}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;overflow-x:hidden;cursor:none}
body::after{content:'';position:fixed;inset:0;z-index:9998;pointer-events:none;opacity:0.035;
background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.cur-d{position:fixed;width:5px;height:5px;background:var(--accent);border-radius:50%;pointer-events:none;z-index:99999;mix-blend-mode:difference}
.cur-r{position:fixed;width:36px;height:36px;border:1px solid rgba(196,163,90,0.4);border-radius:50%;pointer-events:none;z-index:99998;transition:width .4s cubic-bezier(.16,1,.3,1),height .4s cubic-bezier(.16,1,.3,1)}
.cur-r.h{width:60px;height:60px;border-color:var(--accent);background:rgba(196,163,90,0.04)}
/* Hand tracking UI */
#camBtn{position:fixed;top:1.5rem;right:clamp(2rem,6vw,5rem);z-index:101;padding:.5rem 1rem;background:rgba(196,163,90,.15);border:1px solid rgba(196,163,90,.3);border-radius:6px;color:var(--accent2);font-size:.7rem;font-weight:500;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;pointer-events:all;transition:all .3s;mix-blend-mode:difference}
#camBtn:hover{background:rgba(196,163,90,.25)}
#camBtn.on{background:var(--accent);color:var(--bg);mix-blend-mode:normal}
#webcamBox{position:fixed;bottom:20px;right:20px;z-index:999;width:180px;border-radius:10px;overflow:hidden;border:1px solid rgba(196,163,90,.2);opacity:0;pointer-events:none;transition:opacity .5s}
#webcamBox.active{opacity:1}
#webcam{width:100%;display:block;transform:scaleX(-1)}
#webcamBox .wlabel{position:absolute;top:6px;left:8px;font-size:.55rem;color:var(--accent);letter-spacing:.08em;text-transform:uppercase;background:rgba(3,3,3,.7);padding:2px 6px;border-radius:3px}
#handDot{position:fixed;width:16px;height:16px;border:2px solid var(--accent);border-radius:50%;z-index:997;pointer-events:none;opacity:0;transition:opacity .2s;box-shadow:0 0 15px rgba(196,163,90,.25)}
#gl{position:fixed;inset:0;z-index:0}
#gl canvas{width:100%!important;height:100%!important}
nav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;justify-content:space-between;align-items:center;padding:1.5rem clamp(2rem,6vw,5rem);mix-blend-mod