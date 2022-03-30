from os import remove
from pathlib import Path
from os.path import exists, getmtime
import pickle, re, tempfile, unicodedata
from typing import Any, Optional
from time import time

class Cache(object):
	def __init__(self):
		self.directory = tempfile.TemporaryDirectory()
	
	def get(self, reference: str) -> Optional[Any]:
		cachename = self.directory.name + '/' + self.slugify(reference) + '.cache'
		if exists(cachename):
			print(time() - getmtime(cachename))
			if (time() - getmtime(cachename)) > 2629743:
				remove(cachename)
				return None
			else:
				#print( "'%s' found in cache (%s left before expiry)." % (reference, ( 2629743 - (time() - getmtime(cachename)) )) )
				return pickle.load( Path( cachename ).open('rb') )
		else:
			return None
	
	def store(self, reference: str, contents: Any) -> None:
		pppp = self.directory.name + '/' + self.slugify(reference) + '.cache'
		with open(pppp, 'wb') as f:
			# I turned myself into a pickle Mortyyyyyy!
			pickle.dump(contents, f, pickle.HIGHEST_PROTOCOL)
	
	def slugify(self, value: str, allow_unicode: bool = False) -> str:
		"""
		Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
		dashes to single dashes. Remove characters that aren't alphanumerics,
		underscores, or hyphens. Convert to lowercase. Also strip leading and
		trailing whitespace, dashes, and underscores.
		Code is from Django - https://github.com/django/django/blob/main/django/utils/text.py
		"""
		value = str(value)
		if allow_unicode:
			value = unicodedata.normalize("NFKC", value)
		else:
			value = (
				unicodedata.normalize("NFKD", value)
				.encode("ascii", "ignore")
				.decode("ascii")
			)
		value = re.sub(r"[^\w\s-]", "", value.lower())
		return re.sub(r"[-\s]+", "-", value).strip("-_")