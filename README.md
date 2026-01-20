# ImGoaTeX

*ImGoaTeX : Improved Graphics and Objectivly more Accessible than TeX*

**ImGoaTex** is a compled programming language written (so far) in python, inspired by LaTex's Beamer library that lets you create beautifull structured presentations that compile directly to HTML, allowing you to use features traditional Beamer's PDFs lacks such as video, embeded websites, animations and more !

![ImGoaTex](https://i.imgur.com/LHcWlXT.png)

# Installation

- **1 )** Clone the repository and `cd` into the directory
```
git clone https://github.com/ArnaudLelievre48/ImGoaTeX
cd ImGoaTeX
```

- **2 )** Install `KaTeX` by running `install.sh` - [ needs `curl` ]
```
chmod +x install.sh
./install.sh
```

- Recommanded : add `ImGoaTeX-compilor.py` to your `PATH` (on Linux):
```
chmod +x ImGoaTeX-compilor.py
touch ~/.local/bin/igtexc
mkdir -p ~/.local/bin
sudo ln -s /absolute/path/to/ImGoaTeX/compilor.py /usr/local/bin/igtexc
```

# First use

If you aded the compilor to your PATH, you may directly use these commands, otherwise run something like `python3 [abspath-to-ImGoaTeX.py] [file].igtex` instead of `igtexc [file].igtex`.

- Create a presentation file such as `main.igtex` and an empty directory `medias`
- You may add your pieces of media (video, images...) in the `medias` folder
- Write your presentation. Here is a presentation example :
```
%title: Simple ImGoaTeX presentation example
%subtitle: My Presentation : YOU are GoaTeX 🐐
%author: Arnaud Lelièvre
%basefontsize: 1.5

\section{ImGoaTeX}
\subsection{Why}

\begin{frame}{ImGoaTeX is a funny name}[align=top]<ZoomIn, MoveRightOut>
ImGoaTeX is a funny name
\pause
ImGoaTeX actually means : *Improved Graphics and Objectivly more Accessible than TeX*
\end{frame}

\begin{frame}{ImGoaTeX idea}[align=top-left]<RotateIn, ZoomOut>
The actual idea of writing another programmaing language comes from the fact that Beamer is kind of a pain to write without copying and pasting from an existing presentation. And I belive the syntax is too heavy in general.
\pause
The other reason, and the most important one is the lack of ability to use video in a LaTeX presentation, and I don't like the equation editor in presentation tools such as **PowerPoint** or **Google Slides**
\end{frame}


\subsection{How}

\begin{frame}{A programming language}[align=right]
Classic compilor with a *parser*, *tokenizor* and so on...
\pause
I use **Katex** to render equations, allowing for equations such as $\int_{\mathbb{R}} e^{-x^2} dx = \sqrt{\pi}$
\pause
I would like to show off the videos and stuff, but this is a simple example so yeah, go read the documentation if you enjoy this so far !
\pause
Just run : **igtexc main.igtex** !
\end{frame}
```
- All you have to do next is to run :
```
igtexc main.igtex
```

You can now open `output.html` and enjoy your first **ImGoaTex** presentation !

# Go further

Read the documentation (when it is finished and published...)
