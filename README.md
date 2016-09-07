This project is inspired by some conversations I had
with my friend David, who I met through the
[Zulip project](https://github.com/zulip/zulip).  I am
using only his first name to protect his privacy and to
avoid conflating his inspiration for my ideas with my
own interpretation/exploration of them.

Zulip is a chat system where humans and bots send messages
to each other.  David and I are imagining a Zulip ecosystem
where humans can easily program bots and see their source
code and dynamically create new bots with little fanfare.
One prerequisite for that is to have some kind of sandboxed
programming language that folks can write in.

This project implements a little programming language called
"messie" that is aimed to be an LCD, Turing-complete language
that can map to more expressive languages like Python/Ruby/JS/Lisp,
but with a little more minimalism and adaptability to a messaging
paradigm.  The name "messie" refers to messaging, not messiness.
The language looks superficially messy, but I am striving to
make the underlying architecture simple and clean.

The language is intended to be minimal in these regards:
- You cannot mutate data structures, only create new ones.
- There are no variables or assignments.
- There are only a small number of built-in functions.
- The only syntax is JSON (sort of).

The language is intended to be complete in these regards:
- You will be able to manipulate all the JSON-serializable types,
such as integers, floats, strings, lists, and dictionaries.
- You can have functions that work on other functions, such
as MAP and APPLY.
- You can create recursive functions like FACTORIAL.
- It's Turing complete, and you can do things like create an HTML table
of factorial values with relative ease.

The language is unique in these respects:
- Functions communicate by passing around JSON data structures as messages.

The language is extendible:
- Because "messie" fundamentally works with messages, the VM could be
extended to work with multiple processes or multiple computers.
- Because "messie" code is just JSON, functions written in "messie" can
be up-ported to faster or more expressive languages like C/Python/Ruby/JS/Lisp.
- Because "messie" code is just JSON, functions written in higher level
languages can be down-ported to "messie" if you subset those languages to use
only functions and immutable types.

The current implemenation of "messie" is in `computer.py`.  The computer
runs "messie" using a VM that is all in-process, but which uses a message
queue to dispatch calculations.   It can handle deeply recursive functions
despite Python's recursion limit, because function dispatch is mediated
through a queue.

The computer currently calculates a bunch of messages to standard output,
and then it also calculates an HTML table of math results that it writes
to `foo.html`.

Here is example HTML output from "messie":

<table border=1>
<tr><td>n</td><td>double</td><td>square</td><td>factorial</td></tr>
<tr><td>5</td><td>10</td><td>25</td><td>120</td></tr>
<tr><td>6</td><td>12</td><td>36</td><td>720</td></tr>
<tr><td>7</td><td>14</td><td>49</td><td>5040</td></tr>
<tr><td>8</td><td>16</td><td>64</td><td>40320</td></tr>
<tr><td>9</td><td>18</td><td>81</td><td>362880</td></tr>
<tr><td>10</td><td>20</td><td>100</td><td>3628800</td></tr>
<tr><td>11</td><td>22</td><td>121</td><td>39916800</td></tr>
<tr><td>12</td><td>24</td><td>144</td><td>479001600</td></tr>
<tr><td>13</td><td>26</td><td>169</td><td>6227020800</td></tr>
</table>

You can see the "program" that created the above table here:

https://github.com/showell/bot_computer/blob/master/commands.py



