(setq-default
 package-selected-packages '(
			     auctex
			     cmake-mode
			     expand-region
			     git-link
			     magit
			     move-text
			     multiple-cursors
			     projectile
			     session
			     tramp-term
			     yaml-mode
			     )
 TeX-install-font-lock 'ignore
 TeX-view-program-list '(("firefox" "firefox %o"))
 TeX-view-program-selection '((output-pdf "firefox"))
 confirm-nonexistent-file-or-buffer nil
 create-lockfiles 0
 header-line-format '("%b")
 ido-auto-merge-work-directories-length -1
 ido-create-new-buffer 'always
 inhibit-startup-message 1
 initial-scratch-message nil
 make-backup-files nil
 mode-line-format nil
 python-fill-docstring-style 'django
 tramp-syntax 'simplified)

(defalias 'yes-or-no-p 'y-or-n-p)

(setenv "PATH" "/usr/local/texlive/2022/bin/x86_64-linux:$PATH" t)
(delete-selection-mode 1)
(electric-indent-mode 1)
(electric-pair-mode 1)
(global-font-lock-mode 0)
(menu-bar-mode 0)
(scroll-bar-mode 0)
(show-paren-mode 1)
(tool-bar-mode 0)
(xterm-mouse-mode 1)

(global-set-key (kbd "C-c t") (lambda () (interactive) (save-buffer nil) (TeX-command-run-all nil)))
(global-set-key (kbd "s-a") 'mark-whole-buffer)
(global-set-key (kbd "s-c") 'kill-ring-save)
(global-set-key (kbd "s-x") 'kill-region)
(global-set-key (kbd "s-v") 'yank)
(global-set-key (kbd "s-f") 'ido-find-file)
(global-set-key (kbd "s-s") 'save-buffer)
(global-set-key (kbd "s-d") (lambda () (interactive) (find-file ".")))
(global-set-key (kbd "M-v") 'yank-pop)
(global-set-key (kbd "C--") 'undo)
(global-set-key (kbd "C-0") 'delete-window)
(global-set-key (kbd "C-\\") 'kill-this-buffer)
(global-set-key (kbd "C-]") 'kill-whole-line)
(global-set-key (kbd "C-c g l") 'git-link)
(global-set-key (kbd "M-<down>") 'move-text-down)
(global-set-key (kbd "M-<up>") 'move-text-up)
(global-set-key (kbd "M-o") 'other-window)
(global-set-key (kbd "M-m") 'mc/mark-all-like-this)
(global-set-key (kbd "M-n") 'mc/mark-next-like-this)

(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

(require 'dired)
(define-key dired-mode-map (kbd "<left>") 'dired-up-directory)
(define-key dired-mode-map (kbd "<right>") 'dired-find-file)

(require 'ido)
(ido-mode 1)
(add-to-list 'ido-ignore-buffers "\\*" t)

(require 'projectile)
(define-key projectile-mode-map (kbd "C-c p") 'projectile-command-map)
(projectile-mode 1)

(require 'session)
(global-set-key (kbd "C-<left>") 'session-jump-to-last-change)
(session-initialize)

(require 'expand-region)
(global-set-key (kbd "M--") 'er/contract-region)
(global-set-key (kbd "M-=") 'er/expand-region)

(require 'recentf)
(recentf-mode 1)
(global-set-key (kbd "C-c r") 'recentf-open-files)

(defun delete-other-buffers ()
  (interactive)
  (mapc 'kill-buffer (remove (current-buffer) (buffer-list))))
(global-set-key (kbd "C-q") #'delete-other-buffers)

(defun set-selection-in-replace ()
  (interactive)
  (if mark-active
      (let ((region (funcall region-extract-function nil)))
	(minibuffer-with-setup-hook
	    (lambda () (insert region))
	  (goto-char (region-beginning))
	  (deactivate-mark)
	  (call-interactively 'query-replace)))
    (call-interactively 'query-replace)))
(global-set-key (kbd "M-%") #'set-selection-in-replace)

(defun set-next-line () (interactive) (move-end-of-line 1) (newline) (indent-for-tab-command))
(global-set-key (kbd "C-<return>") #'set-next-line)

(defun delete-surrounding-whitespace ()
  (interactive)
  (delete-region
   (progn (re-search-backward "[^[:space:]\n]") (forward-char) (point))
   (progn (re-search-forward "[^[:space:]\n]") (backward-char) (point))))
(global-set-key (kbd "C-'") #'delete-surrounding-whitespace)

(defun duplicate-current-line ()
  (interactive)
  (move-beginning-of-line 1) (kill-line)
  (yank) (open-line 1) (next-line 1) (yank)
  (move-beginning-of-line 1))
(global-set-key (kbd "M-]") #'duplicate-current-line)

(setq termstring "i3-msg exec 'xterm -e /bin/bash --init-file <(echo \". .bashrc && cd %s\")'")
(global-set-key (kbd "C-c e") (lambda () (interactive) (shell-command (format termstring (eval default-directory)))))

(add-hook 'dired-mode-hook (lambda () (dired-hide-details-mode)))
(add-hook 'LaTeX-mode-hook (electric-indent-local-mode 0))
(add-hook 'tex-mode-hook (electric-indent-local-mode 0))

(defun save-all () (interactive) (save-some-buffers t))
(add-hook 'focus-out-hook 'save-all)

(defun set-selection-in-search ()
  (when mark-active
    (deactivate-mark)
    (isearch-push-state)
    (isearch-yank-string (funcall region-extract-function nil))))
(add-hook 'isearch-mode-hook #'set-selection-in-search)

(set-face-background 'region "grey")
(set-face-foreground 'region "black")
