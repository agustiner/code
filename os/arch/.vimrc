set mouse=
set ttymouse=
set clipboard=unnamedplus

function! ClipboardYank()
  call system('xclip -i -selection clipboard', @@)
endfunction

let vlcb = 0
let vlce = 0
function! ClipboardPaste(mode)
  if (a:mode == "v")
    call cursor(g:vlcb[0], g:vlcb[1]) | execute "normal! v" | call cursor(g:vlce[0], g:vlce[1])  
  endif
  let @@ = system('xclip -o -selection clipboard')
endfunction

" replace currently selected text with default register without yanking it
vnoremap <silent>p "_dP

vnoremap <silent>y y:call ClipboardYank()<CR>
vnoremap <silent>d d:call ClipboardYank()<CR>
nnoremap <silent>dd dd:call ClipboardYank()<CR>

nnoremap <silent>p :call ClipboardPaste("n")<CR>p
vnoremap p :<C-U>let vlcb = getpos("'<")[1:2] \| let vlce = getpos("'>")[1:2] \| call ClipboardPaste("v")<CR>p

