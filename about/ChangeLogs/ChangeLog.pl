#! /usr/bin/perl -w

use strict;


if ($#ARGV != 0) {
	print "Usage: $0 ChangeLog\n";
	exit 1;
}


my ($inlist, $inlistitem, $inpara, $inspace);

my $logcount = 0;
my $filecount = 0;

my $filename = $ARGV[0];

sub newfile {
	$filecount++;

	open OUT, ">$filename.$filecount.html";
	
	print OUT '<!--#include virtual="/includes/header_pretitle.inc" -->';
	print OUT "\n<title>$filename</title>\n";
	print OUT '<!--#include virtual="/includes/header_posttitle.inc" -->', "\n";
	print OUT '<!--#include virtual="/includes/menu.inc" -->';
	print OUT "<div class=\"heading\">$filename</div>\n";
	print OUT "<p>Page $filecount</p>\n";

	$inlist = $inlistitem = $inpara = $inspace = 0;
}	

sub endfile {
	my $last = shift;

	print OUT "</p>" if $inpara;
	print OUT "</li>" if $inlistitem;
	print OUT "</ul>" if $inlist;

	print OUT "<p><a href=\"$filename." . ($filecount - 1) . '.html">Previous Page</a> ' unless $filecount == 1;
	print OUT "<a href=\"$filename." . ($filecount + 1) . '.html">Next Page</a></p>' unless $last;
	
	print OUT "<!--#include virtual=\"/includes/linkbar.inc\" -->\n";
	print OUT "<!--#include virtual=\"/includes/footer.inc\" -->";
}

newfile;

while (<>) {
	if (/^[^\s]/) {
		print OUT "</li>" if $inlistitem;
		print OUT "</ul>" if $inlist;
		print OUT "</p>" if $inpara;

		if ($logcount == 10) {
			$logcount = 0;
			endfile 0;
			newfile;
		}

		$logcount++;
		print OUT "<div class=\"subtitle\">$_</div><ul>";
		$inlist = 1;
		$inlistitem = 0;
		$inspace = 0;
		
	} elsif (/^\t\*(.*)/ || /^        \*(.*)/) {
		if ($inspace) {
			print OUT "</li>" if $inlistitem;
			print OUT "</ul>" if $inlist;
			$inlistitem = 0;
			$inlist = 0;
		}
		
		print OUT "</p>" if $inpara;
		print OUT "</li>" if $inlistitem;
		print OUT "<ul>" if !$inlist;
		print OUT "<li>$1\n";
		$inlist = 1;
		$inlistitem = 1;
		$inspace = 0;

	} elsif (/^\t\s*[^\s]/ || /^        \s*[^\s]/) {
		if ($inspace) {
			print OUT "<p>" if !$inpara;
			$inpara = 1;
		}
		
		print OUT $_;
		$inspace = 0;
	} elsif (/^\s*$/) {
		if ($inpara) {
			print OUT "</p>\n";
			$inpara = 0;
		}
		$inspace = 1 if $inlistitem;
	} else {
		warn "Unhandled text";
		print OUT $_;
	}
}

endfile 1;
