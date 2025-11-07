#!/usr/bin/env python3
"""
Hendersonville Counseling - Content Creation CLI
Interactive menu-based interface for weekly content generation
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from create_weekly_batch_v2 import InteractiveWeeklyBatchCreator

# ANSI color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class ContentCreationMenu:
    """Interactive menu system for content creation."""

    def __init__(self):
        self.creator = InteractiveWeeklyBatchCreator()
        self.project_root = Path(__file__).parent
        self.batches_folder = self.project_root / "weekly-batches"

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self):
        """Print the application header."""
        print(f"\n{Colors.CYAN}{'='*80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.HEADER}")
        print("  ██╗  ██╗███████╗███╗   ██╗██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗")
        print("  ██║  ██║██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║")
        print("  ███████║█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║")
        print("  ██╔══██║██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║")
        print("  ██║  ██║███████╗██║ ╚████║██████╔╝███████╗██║  ██║███████║╚██████╔╝██║ ╚████║")
        print("  ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝")
        print(f"{Colors.END}")
        print(f"{Colors.CYAN}                        COUNSELING CONTENT CREATOR{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")

    def print_menu(self, title, options, show_back=True):
        """Print a menu with options."""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
        print(f"{Colors.BLUE}{'-'*len(title)}{Colors.END}\n")

        for i, option in enumerate(options, 1):
            print(f"  {Colors.GREEN}{i}.{Colors.END} {option}")

        if show_back:
            print(f"\n  {Colors.YELLOW}B.{Colors.END} Back to Main Menu")
        print(f"  {Colors.RED}Q.{Colors.END} Quit\n")

    def get_input(self, prompt, valid_options=None):
        """Get user input with validation."""
        while True:
            try:
                user_input = input(f"{Colors.CYAN}{prompt}{Colors.END}").strip()

                if valid_options and user_input.upper() not in valid_options:
                    print(f"{Colors.RED}❌ Invalid option. Please try again.{Colors.END}")
                    continue

                return user_input
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Operation cancelled.{Colors.END}")
                return None

    def get_week_date(self):
        """Get week start date from user."""
        print(f"\n{Colors.BOLD}Week Selection{Colors.END}")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━{Colors.END}\n")

        # Show next few Monday dates as suggestions
        today = datetime.now()
        next_monday = today + timedelta(days=(7 - today.weekday()) % 7)

        print(f"{Colors.YELLOW}📅 Suggested upcoming Mondays:{Colors.END}")
        for i in range(4):
            monday = next_monday + timedelta(weeks=i)
            week_num = monday.isocalendar()[1]
            print(f"  {i+1}. Week {week_num}: {monday.strftime('%Y-%m-%d (%B %d)')}")

        print(f"\n  {Colors.CYAN}Or enter custom date{Colors.END}")

        while True:
            choice = input(f"\n{Colors.CYAN}Enter choice (1-4) or date (YYYY-MM-DD): {Colors.END}").strip()

            # Check if it's a number 1-4
            if choice in ['1', '2', '3', '4']:
                weeks_ahead = int(choice) - 1
                selected_date = next_monday + timedelta(weeks=weeks_ahead)
                return selected_date.strftime('%Y-%m-%d')

            # Try parsing as date
            try:
                parsed_date = datetime.strptime(choice, '%Y-%m-%d')
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                print(f"{Colors.RED}❌ Invalid format. Use YYYY-MM-DD or choose 1-4.{Colors.END}")

    def create_weekly_content(self):
        """Create new weekly content."""
        self.clear_screen()
        self.print_header()

        print(f"{Colors.BOLD}{Colors.GREEN}CREATE NEW WEEKLY CONTENT{Colors.END}")
        print(f"{Colors.GREEN}{'='*80}{Colors.END}\n")

        # Get week date
        week_date = self.get_week_date()
        if not week_date:
            return

        week_dt = datetime.strptime(week_date, '%Y-%m-%d')
        week_num = week_dt.isocalendar()[1]

        print(f"\n{Colors.GREEN}✓ Week {week_num} selected: {week_date}{Colors.END}")

        # Ask about blog
        print(f"\n{Colors.BOLD}Content Options{Colors.END}")
        print(f"{Colors.BLUE}━━━━━━━━━━━━━━━{Colors.END}\n")

        blog_choice = self.get_input(
            "Include blog post with social content? (Y/n): ",
            ['Y', 'N', 'YES', 'NO', '']
        )

        if blog_choice is None:
            return

        with_blog = blog_choice.upper() in ['Y', 'YES', '']

        # Confirm API key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print(f"\n{Colors.RED}❌ Error: ANTHROPIC_API_KEY not found in environment{Colors.END}")
            print(f"{Colors.YELLOW}Please set up your API key first.{Colors.END}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return

        # Start content creation
        print(f"\n{Colors.BOLD}{Colors.GREEN}Starting content creation...{Colors.END}\n")
        print(f"{Colors.YELLOW}This will take 5-10 minutes. You'll be asked to:{Colors.END}")
        print(f"  1. Choose your weekly theme")
        print(f"  2. Select content style (tone, length, audience)")
        print(f"  3. Claude will generate all content\n")

        proceed = self.get_input("Ready to proceed? (Y/n): ", ['Y', 'N', 'YES', 'NO', ''])
        if proceed and proceed.upper() in ['N', 'NO']:
            return

        # Run the creator
        try:
            self.creator.create_interactive_batch(
                week_start=week_date,
                with_blog=with_blog
            )

            print(f"\n{Colors.GREEN}{'='*80}{Colors.END}")
            print(f"{Colors.BOLD}{Colors.GREEN}✓ CONTENT CREATION COMPLETE!{Colors.END}")
            print(f"{Colors.GREEN}{'='*80}{Colors.END}\n")

            input(f"\n{Colors.CYAN}Press Enter to return to main menu...{Colors.END}")

        except Exception as e:
            print(f"\n{Colors.RED}❌ Error during content creation: {str(e)}{Colors.END}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

    def view_existing_content(self):
        """View existing weekly batches."""
        self.clear_screen()
        self.print_header()

        print(f"{Colors.BOLD}{Colors.BLUE}EXISTING WEEKLY CONTENT{Colors.END}")
        print(f"{Colors.BLUE}{'='*80}{Colors.END}\n")

        # List existing weeks
        if not self.batches_folder.exists():
            print(f"{Colors.YELLOW}No content batches found yet.{Colors.END}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return

        week_folders = sorted([f for f in self.batches_folder.iterdir() if f.is_dir()])

        if not week_folders:
            print(f"{Colors.YELLOW}No content batches found yet.{Colors.END}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return

        print(f"{Colors.GREEN}Found {len(week_folders)} week(s):{Colors.END}\n")

        for i, folder in enumerate(week_folders, 1):
            week_name = folder.name
            summary_file = folder / f"WEEK_{week_name.split('-')[-1].upper()}_CONTENT_SUMMARY.md"

            if summary_file.exists():
                status = f"{Colors.GREEN}✓ Complete{Colors.END}"
            else:
                status = f"{Colors.YELLOW}⚠ Incomplete{Colors.END}"

            print(f"  {Colors.CYAN}{i}.{Colors.END} {week_name} - {status}")

            # Check for images
            images_folder = folder / "images"
            if images_folder.exists() and list(images_folder.glob("*")):
                image_count = len(list(images_folder.glob("*")))
                print(f"     {Colors.GREEN}📸 {image_count} image(s){Colors.END}")
            else:
                print(f"     {Colors.YELLOW}📸 No images yet{Colors.END}")

        print(f"\n{Colors.BOLD}Options:{Colors.END}")
        print(f"  {Colors.CYAN}#.{Colors.END} Enter week number to open folder")
        print(f"  {Colors.GREEN}A.{Colors.END} Open all weeks folder")
        print(f"  {Colors.YELLOW}B.{Colors.END} Back to main menu")

        choice = input(f"\n{Colors.CYAN}Enter choice: {Colors.END}").strip().upper()

        if choice == 'B':
            return
        elif choice == 'A':
            os.system(f'open "{self.batches_folder}"')
        elif choice.isdigit() and 1 <= int(choice) <= len(week_folders):
            selected_folder = week_folders[int(choice) - 1]
            os.system(f'open "{selected_folder}"')
        else:
            print(f"{Colors.RED}❌ Invalid choice{Colors.END}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

    def generate_images_menu(self):
        """Guide for generating images for existing content."""
        self.clear_screen()
        self.print_header()

        print(f"{Colors.BOLD}{Colors.YELLOW}IMAGE GENERATION GUIDE{Colors.END}")
        print(f"{Colors.YELLOW}{'='*80}{Colors.END}\n")

        # List weeks without images
        if not self.batches_folder.exists():
            print(f"{Colors.YELLOW}No content batches found yet.{Colors.END}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return

        week_folders = sorted([f for f in self.batches_folder.iterdir() if f.is_dir()])

        print(f"{Colors.GREEN}Weeks needing images:{Colors.END}\n")

        needs_images = []
        for folder in week_folders:
            images_folder = folder / "images"
            if not images_folder.exists() or not list(images_folder.glob("*")):
                needs_images.append(folder)
                week_name = folder.name
                print(f"  {Colors.YELLOW}•{Colors.END} {week_name}")

        if not needs_images:
            print(f"{Colors.GREEN}✓ All weeks have images!{Colors.END}")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            return

        print(f"\n{Colors.BOLD}Quick Image Creation Workflow:{Colors.END}")
        print(f"{Colors.BLUE}{'─'*80}{Colors.END}")
        print(f"\n1. Open the week folder")
        print(f"2. Open QUICK_IMAGE_PROMPT.txt")
        print(f"3. Copy prompt → Paste into ChatGPT or Canva AI")
        print(f"4. Upload to Canva → Use 'Resize' for all formats")
        print(f"5. Add text overlays → Export to images/ folder")
        print(f"\n{Colors.GREEN}⏱️  Total time: 15 minutes{Colors.END}\n")

        print(f"\n{Colors.BOLD}Open a week folder to start:{Colors.END}")
        for i, folder in enumerate(needs_images, 1):
            print(f"  {Colors.CYAN}{i}.{Colors.END} {folder.name}")

        choice = input(f"\n{Colors.CYAN}Enter choice (or B for back): {Colors.END}").strip()

        if choice.upper() == 'B':
            return
        elif choice.isdigit() and 1 <= int(choice) <= len(needs_images):
            selected_folder = needs_images[int(choice) - 1]
            os.system(f'open "{selected_folder}"')
            print(f"\n{Colors.GREEN}✓ Opening {selected_folder.name}{Colors.END}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

    def system_info(self):
        """Show system information."""
        self.clear_screen()
        self.print_header()

        print(f"{Colors.BOLD}{Colors.CYAN}SYSTEM INFORMATION{Colors.END}")
        print(f"{Colors.CYAN}{'='*80}{Colors.END}\n")

        # Check API key
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        api_status = f"{Colors.GREEN}✓ Configured{Colors.END}" if api_key else f"{Colors.RED}✗ Not found{Colors.END}"

        # Count weeks
        week_count = 0
        if self.batches_folder.exists():
            week_count = len([f for f in self.batches_folder.iterdir() if f.is_dir()])

        # Count images
        total_images = 0
        if self.batches_folder.exists():
            for week_folder in self.batches_folder.iterdir():
                if week_folder.is_dir():
                    images_folder = week_folder / "images"
                    if images_folder.exists():
                        total_images += len(list(images_folder.glob("*")))

        print(f"{Colors.BOLD}Status:{Colors.END}")
        print(f"  API Key: {api_status}")
        print(f"  Content Batches: {Colors.GREEN}{week_count}{Colors.END}")
        print(f"  Total Images: {Colors.GREEN}{total_images}{Colors.END}")

        print(f"\n{Colors.BOLD}Paths:{Colors.END}")
        print(f"  Project: {self.project_root}")
        print(f"  Content: {self.batches_folder}")

        print(f"\n{Colors.BOLD}Documentation:{Colors.END}")
        print(f"  • TEAM_EXECUTION_CHECKLIST.md - Main workflow guide")
        print(f"  • CANVA_WORKFLOW_SYSTEM.md - Image creation guide")
        print(f"  • README.md - Project overview")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")

    def main_menu(self):
        """Display and handle main menu."""
        while True:
            self.clear_screen()
            self.print_header()

            print(f"{Colors.BOLD}What would you like to do?{Colors.END}\n")

            options = [
                "🆕 Create New Weekly Content (8 posts + blog)",
                "📁 View Existing Content",
                "🖼️  Generate Images for Content",
                "ℹ️  System Information",
            ]

            for i, option in enumerate(options, 1):
                print(f"  {Colors.GREEN}{i}.{Colors.END} {option}")

            print(f"\n  {Colors.RED}Q.{Colors.END} Quit\n")

            choice = self.get_input("Enter your choice: ", ['1', '2', '3', '4', 'Q'])

            if choice is None or choice.upper() == 'Q':
                print(f"\n{Colors.CYAN}👋 Goodbye!{Colors.END}\n")
                sys.exit(0)

            if choice == '1':
                self.create_weekly_content()
            elif choice == '2':
                self.view_existing_content()
            elif choice == '3':
                self.generate_images_menu()
            elif choice == '4':
                self.system_info()


def main():
    """Entry point for the CLI."""
    try:
        menu = ContentCreationMenu()
        menu.main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}👋 Goodbye!{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error: {str(e)}{Colors.END}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
