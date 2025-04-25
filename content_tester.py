#!/usr/bin/env python3
"""
Blog Content Quality and SEO Tester

This script tests the quality and SEO effectiveness of generated blog content
for insurance claims advocacy.
"""

import os
import json
import argparse
import re
import sys
import random
from datetime import datetime

# Add the current directory to the path to import other modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from blog_generator import BlogContentGenerator

class ContentTester:
    """
    A class to test blog content quality and SEO effectiveness.
    """
    
    def __init__(self, data_dir="/home/ubuntu/blog_automation"):
        """
        Initialize the ContentTester.
        
        Args:
            data_dir (str): Directory containing blog data files
        """
        self.data_dir = data_dir
        self.content_dir = os.path.join(data_dir, "generated_content")
        self.test_dir = os.path.join(data_dir, "test_results")
        self.keywords_file = os.path.join(data_dir, "seo_keywords.md")
        
        # Create test directory if it doesn't exist
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Initialize the content generator
        self.generator = BlogContentGenerator(data_dir=data_dir)
        
        # Load keywords
        self.keywords = self._load_keywords()
        
        print(f"ContentTester initialized with data from {data_dir}")
    
    def _load_keywords(self):
        """
        Load SEO keywords from the keywords file.
        
        Returns:
            dict: Dictionary of keyword categories and lists
        """
        keywords = {
            "primary": [],
            "secondary": [],
            "long_tail": [],
            "semantic": []
        }
        
        try:
            with open(self.keywords_file, 'r') as f:
                content = f.read()
            
            # Extract primary keywords
            primary_match = re.search(r'## Primary Keywords\n\n(.*?)(?=\n\n##)', content, re.DOTALL)
            if primary_match:
                primary_text = primary_match.group(1)
                keywords["primary"] = [k.strip()[3:] for k in primary_text.split('\n') if k.strip().startswith('-') or k.strip().startswith('1.')]
            
            # Extract secondary keywords (combine all categories)
            secondary_categories = [
                "Storm Types and Damage",
                "Claims Process",
                "Advocacy and Support",
                "Financial Terms",
                "Consumer Education"
            ]
            
            for category in secondary_categories:
                section_match = re.search(f'### {category}\n(.*?)(?=\n\n###|\n\n##|$)', content, re.DOTALL)
                if section_match:
                    section_text = section_match.group(1)
                    keywords["secondary"].extend([k.strip()[2:] for k in section_text.split('\n') if k.strip().startswith('-')])
            
            # Extract long-tail keywords
            longtail_match = re.search(r'## Long-Tail Keywords\n\n(.*?)(?=\n\n##|$)', content, re.DOTALL)
            if longtail_match:
                longtail_text = longtail_match.group(1)
                keywords["long_tail"] = [k.strip()[3:].strip('"') for k in longtail_text.split('\n') if k.strip().startswith('-') or k.strip().startswith('1.')]
            
            # Extract semantic keywords
            semantic_match = re.search(r'## Semantic Keywords and Related Terms\n\n(.*?)(?=$)', content, re.DOTALL)
            if semantic_match:
                semantic_text = semantic_match.group(1)
                keywords["semantic"] = [k.strip()[2:] for k in semantic_text.split('\n') if k.strip().startswith('-')]
            
            print(f"Loaded {len(keywords['primary'])} primary keywords, {len(keywords['secondary'])} secondary keywords, {len(keywords['long_tail'])} long-tail keywords, and {len(keywords['semantic'])} semantic keywords")
            return keywords
        
        except Exception as e:
            print(f"Error loading keywords: {e}")
            return keywords
    
    def test_blog_post(self, blog_file):
        """
        Test the quality and SEO effectiveness of a blog post.
        
        Args:
            blog_file (str): Path to the blog post file (JSON or Markdown)
        
        Returns:
            dict: Test results
        """
        # Load blog post content
        content = self._load_blog_content(blog_file)
        if not content:
            return None
        
        # Run tests
        results = {
            "file": blog_file,
            "timestamp": datetime.now().isoformat(),
            "word_count": self._test_word_count(content),
            "keyword_usage": self._test_keyword_usage(content),
            "readability": self._test_readability(content),
            "structure": self._test_structure(content),
            "overall_score": 0
        }
        
        # Calculate overall score
        results["overall_score"] = self._calculate_overall_score(results)
        
        # Save results
        self._save_test_results(results)
        
        return results
    
    def _load_blog_content(self, blog_file):
        """
        Load blog post content from a file.
        
        Args:
            blog_file (str): Path to the blog post file (JSON or Markdown)
        
        Returns:
            str: Blog post content
        """
        try:
            if blog_file.endswith('.json'):
                with open(blog_file, 'r') as f:
                    blog_post = json.load(f)
                
                # Extract content from JSON structure
                content = blog_post.get('title', '') + '\n\n'
                content += blog_post.get('introduction', '') + '\n\n'
                
                for section in blog_post.get('sections', []):
                    content += section.get('heading', '') + '\n\n'
                    content += section.get('content', '') + '\n\n'
                
                if 'tips' in blog_post:
                    content += blog_post['tips'].get('intro', '') + '\n\n'
                    for tip in blog_post['tips'].get('list', []):
                        content += '- ' + tip + '\n'
                    content += '\n\n'
                
                if 'downloadable_resource' in blog_post:
                    content += 'Free Resource: ' + blog_post['downloadable_resource'].get('title', '') + '\n\n'
                    content += blog_post['downloadable_resource'].get('description', '') + '\n\n'
                
                content += blog_post.get('conclusion', '') + '\n\n'
                
                for faq in blog_post.get('faq', []):
                    content += faq.get('question', '') + '\n\n'
                    content += faq.get('answer', '') + '\n\n'
                
                return content
            
            elif blog_file.endswith('.md'):
                with open(blog_file, 'r') as f:
                    content = f.read()
                
                # Remove image suggestion comments
                content = re.sub(r'<!-- Image Suggestions:.*?-->', '', content, flags=re.DOTALL)
                
                return content
            
            else:
                print(f"Unsupported file format: {blog_file}")
                return None
        
        except Exception as e:
            print(f"Error loading blog post: {e}")
            return None
    
    def _test_word_count(self, content):
        """
        Test the word count of the blog post.
        
        Args:
            content (str): Blog post content
        
        Returns:
            dict: Word count test results
        """
        # Count words
        words = re.findall(r'\b\w+\b', content)
        word_count = len(words)
        
        # Evaluate against target range (1000-1500 words)
        if 1000 <= word_count <= 1500:
            status = "Excellent"
            score = 10
        elif 800 <= word_count < 1000 or 1500 < word_count <= 1800:
            status = "Good"
            score = 8
        elif 600 <= word_count < 800 or 1800 < word_count <= 2000:
            status = "Acceptable"
            score = 6
        else:
            status = "Needs Improvement"
            score = 4
        
        return {
            "count": word_count,
            "target_range": "1000-1500",
            "status": status,
            "score": score
        }
    
    def _test_keyword_usage(self, content):
        """
        Test the keyword usage in the blog post.
        
        Args:
            content (str): Blog post content
        
        Returns:
            dict: Keyword usage test results
        """
        # Convert content to lowercase for case-insensitive matching
        content_lower = content.lower()
        
        # Count keyword occurrences
        keyword_counts = {
            "primary": {},
            "secondary": {},
            "long_tail": {},
            "semantic": {}
        }
        
        # Check primary keywords
        for keyword in self.keywords["primary"]:
            count = content_lower.count(keyword.lower())
            if count > 0:
                keyword_counts["primary"][keyword] = count
        
        # Check secondary keywords
        for keyword in self.keywords["secondary"]:
            count = content_lower.count(keyword.lower())
            if count > 0:
                keyword_counts["secondary"][keyword] = count
        
        # Check long-tail keywords
        for keyword in self.keywords["long_tail"]:
            count = content_lower.count(keyword.lower())
            if count > 0:
                keyword_counts["long_tail"][keyword] = count
        
        # Check semantic keywords
        for keyword in self.keywords["semantic"]:
            count = content_lower.count(keyword.lower())
            if count > 0:
                keyword_counts["semantic"][keyword] = count
        
        # Calculate statistics
        primary_used = len(keyword_counts["primary"])
        secondary_used = len(keyword_counts["secondary"])
        long_tail_used = len(keyword_counts["long_tail"])
        semantic_used = len(keyword_counts["semantic"])
        
        total_keywords_used = primary_used + secondary_used + long_tail_used + semantic_used
        
        # Calculate keyword density
        word_count = len(re.findall(r'\b\w+\b', content))
        total_keyword_occurrences = sum(sum(category.values()) for category in keyword_counts.values())
        keyword_density = (total_keyword_occurrences / word_count) * 100 if word_count > 0 else 0
        
        # Evaluate keyword usage
        if primary_used >= 2 and secondary_used >= 5 and long_tail_used >= 1 and 1.0 <= keyword_density <= 3.0:
            status = "Excellent"
            score = 10
        elif primary_used >= 1 and secondary_used >= 3 and 0.5 <= keyword_density <= 4.0:
            status = "Good"
            score = 8
        elif primary_used >= 1 and secondary_used >= 2 and keyword_density <= 5.0:
            status = "Acceptable"
            score = 6
        else:
            status = "Needs Improvement"
            score = 4
        
        return {
            "primary_keywords": {
                "used": primary_used,
                "total": len(self.keywords["primary"]),
                "details": keyword_counts["primary"]
            },
            "secondary_keywords": {
                "used": secondary_used,
                "total": len(self.keywords["secondary"]),
                "details": keyword_counts["secondary"]
            },
            "long_tail_keywords": {
                "used": long_tail_used,
                "total": len(self.keywords["long_tail"]),
                "details": keyword_counts["long_tail"]
            },
            "semantic_keywords": {
                "used": semantic_used,
                "total": len(self.keywords["semantic"]),
                "details": keyword_counts["semantic"]
            },
            "total_keywords_used": total_keywords_used,
            "keyword_density": round(keyword_density, 2),
            "optimal_density_range": "1.0-3.0%",
            "status": status,
            "score": score
        }
    
    def _test_readability(self, content):
        """
        Test the readability of the blog post.
        
        Args:
            content (str): Blog post content
        
        Returns:
            dict: Readability test results
        """
        # Count sentences
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Count words
        words = re.findall(r'\b\w+\b', content)
        word_count = len(words)
        
        # Count syllables (simplified approximation)
        syllable_count = 0
        for word in words:
            word = word.lower()
            if len(word) <= 3:
                syllable_count += 1
                continue
                
            # Count vowel groups as syllables
            vowels = "aeiouy"
            count = 0
            prev_is_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not prev_is_vowel:
                    count += 1
                prev_is_vowel = is_vowel
            
            # Adjust for common patterns
            if word.endswith('e'):
                count -= 1
            if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
                count += 1
            if count == 0:
                count = 1
                
            syllable_count += count
        
        # Calculate average sentence length
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # Calculate average syllables per word
        avg_syllables_per_word = syllable_count / word_count if word_count > 0 else 0
        
        # Calculate Flesch Reading Ease score (simplified)
        # Formula: 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        flesch_score = max(0, min(100, flesch_score))  # Clamp to 0-100 range
        
        # Evaluate readability
        if 60 <= flesch_score <= 70:
            status = "Excellent"
            score = 10
        elif 50 <= flesch_score < 60 or 70 < flesch_score <= 80:
            status = "Good"
            score = 8
        elif 40 <= flesch_score < 50 or 80 < flesch_score <= 90:
            status = "Acceptable"
            score = 6
        else:
            status = "Needs Improvement"
            score = 4
        
        # Determine reading level
        if flesch_score >= 90:
            reading_level = "5th grade (Very easy to read)"
        elif flesch_score >= 80:
            reading_level = "6th grade (Easy to read)"
        elif flesch_score >= 70:
            reading_level = "7th grade (Fairly easy to read)"
        elif flesch_score >= 60:
            reading_level = "8th-9th grade (Plain English)"
        elif flesch_score >= 50:
            reading_level = "10th-12th grade (Fairly difficult)"
        elif flesch_score >= 30:
            reading_level = "College (Difficult)"
        else:
            reading_level = "College graduate (Very difficult)"
        
        return {
            "sentence_count": sentence_count,
            "word_count": word_count,
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_word_length": round(avg_word_length, 1),
            "avg_syllables_per_word": round(avg_syllables_per_word, 1),
            "flesch_reading_ease": round(
(Content truncated due to size limit. Use line ranges to read in chunks)