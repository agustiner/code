(setq-default
 package-selected-packages '(move-text
			     expand-region
			     multiple-cursors
			     yaml-mode
			     auctex
			     git-link
			     xclip
			     projectile
			     tramp-term
			     session
			     magit
			     cmake-mode)
 TeX-install-font-lock 'ignore
 TeX-view-program-list '(("firefox" "firefox %o"))
 TeX-view-program-selection '((output-pdf "firefox"))
 create-lockfiles 0
 header-line-format '("%b")
 ido-auto-merge-work-directories-length -1
 inhibit-startup-message 1
 initial-scratch-message nil
 confirm-nonexistent-file-or-buffer nil
 ido-create-new-buffer 'always
 make-backup-files nil
 mode-line-format nil
 python-fill-docstring-style 'django
 ring-bell-function 'ignore
 tramp-syntax 'simplified
 truncate-lines 1
 )
(defalias 'yes-or-no-p 'y-or-n-p)

(global-set-key (kbd "C-c t") (lambda () (interactive) (save-buffer nil) (TeX-command-run-all nil)))
(global-set-key (kbd "s-c") 'kill-ring-save)
(global-set-key (kbd "s-x") 'kill-region)
(global-set-key (kbd "s-v") 'yank)
(global-set-key (kbd "M-v") 'yank-pop)
(global-set-key (kbd "C--") 'undo)
(global-set-key (kbd "C-0") 'delete-window)
(global-set-key (kbd "C-\\") 'kill-this-buffer)
(global-set-key (kbd "C-]") 'kill-whole-line)
(global-set-key (kbd "C-c g l") 'git-link)
(global-set-key (kbd "M-<down>") 'move-text-down)
(global-set-key (kbd "M-<up>") 'move-text-up)
(global-set-key (kbd "M-o") 'other-window)
(global-set-key (kbd "C-<return>") (lambda () (interactive)
				     (move-end-of-line 1)
				     (newline)))
(global-set-key (kbd "M-m") 'mc/mark-all-like-this)
(global-set-key (kbd "M-n") 'mc/mark-next-like-this)
(global-set-key (kbd "C-'") (lambda () (interactive)
			       (delete-region
				(progn (re-search-backward "[^[:space:]\n]") (forward-char) (point))
				(progn (re-search-forward "[^[:space:]\n]") (backward-char) (point)))))
(global-set-key (kbd "M-]") (lambda () (interactive)
			      (move-beginning-of-line 1)
			      (kill-line)
			      (yank)
			      (open-line 1)
			      (next-line 1)
			      (yank)
			      (move-beginning-of-line 1)))

(require 'dired)
(define-key dired-mode-map (kbd "<left>") 'dired-up-directory)
(define-key dired-mode-map (kbd "<right>") 'dired-find-file)

(require 'package)
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
(package-initialize)

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

(defun set-solo-buffer ()
  (interactive)
  (mapc 'kill-buffer (remove (current-buffer) (buffer-list))))
(global-set-key (kbd "C-q") #'set-solo-buffer)

(defun set-selection-in-search ()
  (when mark-active
    (deactivate-mark)
    (isearch-push-state)
    (isearch-yank-string (funcall region-extract-function nil))))
(add-hook 'isearch-mode-hook #'set-selection-in-search)

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

(add-hook 'dired-mode-hook
      (lambda () (dired-hide-details-mode)))

(defun set-no-indent ()
  (electric-indent-local-mode -1))
(add-hook 'LaTeX-mode-hook 'set-no-indent)
(add-hook 'tex-mode-hook 'set-no-indent)

(defun set-clipboard-in-find-file ()
  (interactive)
  (if (and (length> kill-ring 0) (file-exists-p (nth 0 kill-ring)))
      (find-file (nth 0 kill-ring))
    (ido-find-file)))
(global-set-key (kbd "C-x C-f") #'set-clipboard-in-find-file)

(defun save-all ()
  (interactive)
  (save-some-buffers t))
(add-hook 'focus-out-hook 'save-all)

(delete-selection-mode 1)
(electric-indent-mode 1)
(electric-pair-mode 1)
(global-font-lock-mode 0)
(menu-bar-mode 0)
(scroll-bar-mode 0)
(show-paren-mode 1)
(tool-bar-mode 0)
(xclip-mode 1)
(xterm-mouse-mode 1)

;; (set-face-foreground 'vertical-border "white")
;; (set-face-background 'vertical-border "white")
;; (set-face-background 'mode-line "grey")
;; (set-face-background 'mode-line-inactive "grey")
;; (set-face-background 'region "grey")
;; (set-face-foreground 'region "white")
;; (set-face-background 'fringe "white")
;; (set-face-attribute 'mode-line nil :box nil)
;; (set-face-attribute 'mode-line-inactive nil :box nil)
;; (set-display-table-slot standard-display-table 'vertical-border ?\ )
;; (set-display-table-slot standard-display-table 0 ?\ )
;; (global-set-key (kbd "C-a") 'back-to-indentation)
;; (global-set-key (kbd "M-f") (lambda () (interactive)
;; 			      (fill-paragraph)
;; 			      (scroll-right (window-hscroll))))
;; (global-set-key (kbd "C-c e") (lambda () (interactive) (shell-command (format "osascript -e 'tell application \"System Events\"' -e 'keystroke \"t\" using command down' -e 'end' -e 'tell application \"Terminal\"' -e 'activate' -e 'do script with command \"cd %s\" in window 1' -e 'end tell'" (eval default-directory)))))
;; (global-set-key (kbd "C-c t") 'tramp-term)
;; (global-set-key (kbd "C-c e") (lambda () (interactive) (shell-command (format "i3-msg exec "xterm -e "bash -c "echo hello"""" (eval default-directory)))))
;; auto-save-interval 0
;; (add-to-list 'projectile-globally-ignored-files "*ipynb")
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(package-selected-packages
   '(cmake-mode mini-frame move-text expand-region multiple-cursors yaml-mode auctex git-link xclip projectile tramp-term session magit))
 '(session-use-package t nil (session)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
;; (setq recentf-max-menu-items 20)
;; (setq recentf-max-saved-items 20)
