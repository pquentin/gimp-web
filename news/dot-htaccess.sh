AddHandler cgi-script .cgi
AuthName "news.gimp.org"
AuthType Digest
AuthDigestFile __NEWSDIR__/.password
AuthDigestDomain /news
Options +Includes
Options +Indexes +ExecCGI +MultiViews +SymLinksIfOwnerMatch +IncludesNoExec
Require valid-user
