import sys
import os
import json
from pathlib import Path

# Add the original blog automation system to the Python path
sys.path.append('/home/ubuntu/blog_automation')

# Import the original blog automation modules
try:
    from blog_generator import BlogGenerator
    from content_tester import ContentTester
    from photo_collection_api import PhotoCollectionAPI
    from damage_assessment import DamageAssessment
    from xactimate_integration import XactimateIntegration
except ImportError as e:
    print(f"Error importing original modules: {e}")

class BlogAutomationAPI:
    """
    API wrapper for the blog automation system.
    This class provides a bridge between the frontend and the original Python modules.
    """
    
    def __init__(self):
        self.blog_generator = None
        self.content_tester = None
        self.initialize_modules()
        
    def initialize_modules(self):
        """Initialize the original blog automation modules"""
        try:
            self.blog_generator = BlogGenerator()
            self.content_tester = ContentTester()
            print("Successfully initialized blog automation modules")
        except Exception as e:
            print(f"Error initializing modules: {e}")
            # Create mock modules for development if original modules can't be loaded
            self.create_mock_modules()
    
    def create_mock_modules(self):
        """Create mock modules for development and testing"""
        class MockBlogGenerator:
            def generate_blog_post(self, topic, template_type, storm_type, target_length, additional_instructions=None):
                return {
                    "title": f"Understanding {storm_type} Damage Insurance Claims",
                    "content": f"This is a mock blog post about {topic} using the {template_type} template.",
                    "word_count": target_length,
                    "seo_score": 85,
                    "keywords": ["insurance claims", "storm damage", "property damage", "claim process"]
                }
        
        class MockContentTester:
            def analyze_content(self, content, target_keywords=None, target_audience=None):
                return {
                    "seo_score": 72,
                    "readability_score": "B+",
                    "keyword_density": 1.8,
                    "detected_keywords": ["insurance claims", "storm damage", "property damage", "claim process", "insurance adjuster"],
                    "suggestions": [
                        "Add more content to reach recommended length",
                        "Optimize title with target keywords",
                        "Add more transition words"
                    ]
                }
        
        self.blog_generator = MockBlogGenerator()
        self.content_tester = MockContentTester()
        print("Created mock modules for development")
    
    def generate_blog_post(self, data):
        """Generate a blog post using the blog generator module"""
        try:
            result = self.blog_generator.generate_blog_post(
                topic=data.get('topic', ''),
                template_type=data.get('template', 'educational'),
                storm_type=data.get('stormType', 'general'),
                target_length=int(data.get('targetLength', 1200)),
                additional_instructions=data.get('additionalInstructions', '')
            )
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def test_content(self, data):
        """Test content using the content tester module"""
        try:
            result = self.content_tester.analyze_content(
                content=data.get('content', ''),
                target_keywords=data.get('targetKeywords', 'auto'),
                target_audience=data.get('targetAudience', '')
            )
            return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_blog_posts(self):
        """Get all blog posts"""
        # In a real implementation, this would fetch from a database
        # For now, return mock data
        posts = [
            {
                "id": "1",
                "title": "Understanding Insurance Claims After Hurricane Damage",
                "status": "published",
                "date": "2025-04-10",
                "seoScore": 85,
                "wordCount": 1245,
                "template": "educational",
                "stormType": "hurricane"
            },
            {
                "id": "2",
                "title": "How to Document Storm Damage for Maximum Claim Value",
                "status": "ready",
                "date": "2025-04-20",
                "seoScore": 92,
                "wordCount": 1350,
                "template": "problem_solution",
                "stormType": "general"
            },
            {
                "id": "3",
                "title": "Working with Public Adjusters: What You Need to Know",
                "status": "draft",
                "date": "2025-04-18",
                "seoScore": 76,
                "wordCount": 980,
                "template": "expert",
                "stormType": "general"
            },
            {
                "id": "4",
                "title": "5 Common Mistakes to Avoid When Filing Storm Damage Claims",
                "status": "draft",
                "date": "2025-04-15",
                "seoScore": 81,
                "wordCount": 1120,
                "template": "problem_solution",
                "stormType": "general"
            }
        ]
        return {"success": True, "data": posts}
    
    def get_scheduled_posts(self):
        """Get scheduled blog posts"""
        # In a real implementation, this would fetch from a database
        # For now, return mock data
        posts = [
            {
                "id": "1",
                "title": "Preparing for Hurricane Season",
                "date": "2025-04-28",
                "status": "scheduled"
            },
            {
                "id": "2",
                "title": "Working with Public Adjusters",
                "date": "2025-05-05",
                "status": "scheduled"
            },
            {
                "id": "3",
                "title": "Understanding Flood Insurance Claims",
                "date": "2025-05-12",
                "status": "scheduled"
            },
            {
                "id": "4",
                "title": "How to Appeal a Denied Claim",
                "date": "2025-05-19",
                "status": "draft"
            }
        ]
        return {"success": True, "data": posts}
    
    def publish_blog_post(self, data):
        """Publish a blog post"""
        try:
            # In a real implementation, this would update the database and trigger publishing
            post_id = data.get('postId')
            destination = data.get('publishDestination', 'website')
            publish_date = data.get('publishDate')
            category = data.get('category', 'insurance-claims')
            tags = data.get('tags', '').split(',')
            
            # Mock successful publishing
            return {"success": True, "message": f"Blog post {post_id} published successfully to {destination}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def schedule_blog_post(self, data):
        """Schedule a blog post for future publishing"""
        try:
            # In a real implementation, this would update the database with scheduling info
            post_id = data.get('blogPost')
            schedule_date = data.get('scheduleDate')
            schedule_time = data.get('scheduleTime', '09:00')
            frequency = data.get('frequency', 'none')
            social_share = data.get('socialShare', 'none')
            
            # Mock successful scheduling
            return {"success": True, "message": f"Blog post {post_id} scheduled for {schedule_date} at {schedule_time}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_blog_post(self, post_id):
        """Get a specific blog post by ID"""
        # In a real implementation, this would fetch from a database
        # For now, return mock data for post ID 1
        if post_id == "1":
            post = {
                "id": "1",
                "title": "Understanding Insurance Claims After Hurricane Damage",
                "content": """
                <h1>Understanding Insurance Claims After Hurricane Damage</h1>
                <p class="lead">When a hurricane strikes, the aftermath can be overwhelming. Beyond the emotional toll of seeing your property damaged, navigating the insurance claims process adds another layer of stress. This comprehensive guide will walk you through the steps of filing and maximizing your hurricane damage insurance claim.</p>
                
                <h2>The Immediate Steps After Hurricane Damage</h2>
                <p>The moments and days following a hurricane are critical for your insurance claim. Here's what you need to do right away:</p>
                <ul>
                    <li><strong>Ensure safety first</strong> - Before assessing damage, make sure your property is safe to enter</li>
                    <li><strong>Document everything</strong> - Take photos and videos of all damage before cleaning up</li>
                    <li><strong>Make temporary repairs</strong> - Prevent further damage, but save all receipts</li>
                    <li><strong>Contact your insurance company</strong> - Report the claim as soon as possible</li>
                </ul>
                
                <h2>Understanding Your Hurricane Coverage</h2>
                <p>Hurricane damage often involves multiple types of insurance coverage:</p>
                <p>Most homeowners are surprised to learn that hurricane damage may be covered under different portions of their policy, or even separate policies altogether. Wind damage is typically covered under your standard homeowner's policy, while flood damage requires separate flood insurance.</p>
                """,
                "status": "published",
                "date": "2025-04-10",
                "seoScore": 85,
                "wordCount": 1245,
                "template": "educational",
                "stormType": "hurricane",
                "metadata": {
                    "metaTitle": "Understanding Insurance Claims After Hurricane Damage | Heartland Claims",
                    "metaDescription": "Learn how to navigate the insurance claims process after hurricane damage. Our comprehensive guide helps homeowners maximize their claim value and avoid common pitfalls.",
                    "focusKeywords": ["hurricane insurance claims", "storm damage insurance", "hurricane damage", "insurance claim process"]
                }
            }
            return {"success": True, "data": post}
        else:
            return {"success": False, "error": "Post not found"}

# Create a simple API handler for the Next.js API routes
def handle_api_request(method, path, data=None):
    """Handle API requests from the frontend"""
    api = BlogAutomationAPI()
    
    # Route the request to the appropriate method
    if path == "/api/blog-posts" and method == "GET":
        return api.get_blog_posts()
    elif path == "/api/blog-posts" and method == "POST":
        return api.generate_blog_post(data)
    elif path.startswith("/api/blog-posts/") and method == "GET":
        post_id = path.split("/")[-1]
        return api.get_blog_post(post_id)
    elif path == "/api/test" and method == "POST":
        return api.test_content(data)
    elif path == "/api/publish" and method == "POST":
        return api.publish_blog_post(data)
    elif path == "/api/schedule" and method == "GET":
        return api.get_scheduled_posts()
    elif path == "/api/schedule" and method == "POST":
        return api.schedule_blog_post(data)
    else:
        return {"success": False, "error": "Invalid API route"}

# For testing the API directly
if __name__ == "__main__":
    # Test the API
    api = BlogAutomationAPI()
    
    # Test blog generation
    test_data = {
        "topic": "Insurance claim process after hurricane damage",
        "template": "educational",
        "stormType": "hurricane",
        "targetLength": 1200,
        "additionalInstructions": "Include information about documentation requirements"
    }
    result = api.generate_blog_post(test_data)
    print(json.dumps(result, indent=2))
    
    # Test content testing
    test_content = """
    Understanding Insurance Claims After Hurricane Damage
    
    When a hurricane strikes, the aftermath can be overwhelming. Beyond the emotional toll of seeing your property damaged, navigating the insurance claims process adds another layer of stress.
    
    The moments and days following a hurricane are critical for your insurance claim. Here's what you need to do right away:
    - Ensure safety first
    - Document everything
    - Make temporary repairs
    - Contact your insurance company
    """
    test_data = {
        "content": test_content,
        "targetKeywords": "auto",
        "targetAudience": "Homeowners affected by storms"
    }
    result = api.test_content(test_data)
    print(json.dumps(result, indent=2))
