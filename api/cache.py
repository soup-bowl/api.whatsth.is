from os import remove
from pathlib import Path
from os.path import exists, getmtime
import pickle, re, tempfile, unicodedata
from typing import Any, Optional
from time import time

class Cache(object):
	def __init__(self):
		self.directory = tempfile.TemporaryDirectory()
		self.cachetime = 2629743

	def get(self, reference: str) -> Optional[Any]:
		"""Get the item reference from the object cache.

		Args:
			reference (str): Name (that will be sanitised) to look for in the object store.

		Returns:
			Optional[Any]: Either the requested object, or None. None also returned if the cache timer expires.
		"""
		cachename = self.directory.name + '/' + self.slugify(reference) + '.cache'
		if exists(cachename):
			print(time() - getmtime(cachename))
			if (time() - getmtime(cachename)) > self.cachetime:
				remove(cachename)
				return None
			else:
				#print( "'%s' found in cache (%s left before expiry)." % (reference, ( self.cachetime - (time() - getmtime(cachename)) )) )
				return pickle.load( Path( cachename ).open('rb') )
		else:
			return None

	def store(self, reference: str, contents: Any) -> None:
		"""Stores the provided contents into the cache with the reference.

		Args:
			reference (str): Sanitised string reference.
			contents (Any): Objec to be cached.
		"""
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