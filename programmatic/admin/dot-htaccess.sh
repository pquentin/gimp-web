AddHandler cgi-script .cgi
AuthName "news.gimp.org"
AuthType Digest
AuthDigestFile __NEWSDIR__/.password
AuthDigestDomain /news
Options +Includes +Indexes +ExecCGI +MultiViews +SymLinksIfOwnerMatch +IncludesNoExec
Require valid-user
