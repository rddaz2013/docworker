from . import doc_convert
from . import section_util
import unittest
import tiktoken

TEXT="""
 Four score and seven years ago our fathers brought forth, upon this continent, a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal.

Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived, and so dedicated, can long endure. We are met on a great battle field of that war. We come to dedicate a portion of it, as a final resting place for those who died here, that the nation might live. This we may, in all propriety do.

But, in a larger sense, we can not dedicate we can not consecrate we can not hallow, this ground The brave men, living and dead, who struggled here, have hallowed it, far above our poor power to add or detract. The world will little note, nor long remember what we say here; while it can never forget what they did here.

It is rather for us, the living, we here be dedicated to the great task remaining before us that, from these honored dead we take increased devotion to that cause for which they here, gave the last full measure of devotion that we here highly resolve these dead shall not have died in vain; that the nation, shall have a new birth of freedom, and that government of the people, by the people, for the people, shall not perish from the earth.
"""

class DocConvertTestCase(unittest.TestCase):

  def testChunking(self):
    tokenizer = tiktoken.encoding_for_model(section_util.AI_MODEL)
    chunks = list(doc_convert.chunks(TEXT, 20, tokenizer))
    self.assertEqual(len(chunks), 15)
    for chunk in chunks:
      self.assertTrue(len(chunk) <= 20)

    
