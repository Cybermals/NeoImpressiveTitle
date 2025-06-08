from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.bubble import Bubble

from ui.theme import GameFloatingWindow

import ui.block_list
import ui.friend_list


# Classes
# =======
class FriendBubble(Bubble):
    friend = ObjectProperty()

    def on_touch_up(self, touch):
        # Call base method
        super().on_touch_down(touch)

        # Handled event?
        if self.collide_point(touch.x, touch.y):
            return True
        
        # Close this widget
        self.parent.remove_widget(self)
        return False
    

class BlockedPlayerBubble(Bubble):
    player = ObjectProperty()

    def on_touch_up(self, touch):
        # Call base method
        super().on_touch_down(touch)

        # Handled event?
        if self.collide_point(touch.x, touch.y):
            return True
        
        # Close this widget
        self.parent.remove_widget(self)
        return False


class FriendsDialog(GameFloatingWindow):
    friends = ObjectProperty()
    blocked_players = ObjectProperty()

    def on_touch_down(self, touch):
        self.mouse_pos = touch.pos
        return super().on_touch_down(touch)

    def on_friends(self, instance, value):
        # Load sample friends
        self.friends.data = [{
            "online": i % 4,
            "username": f"Friend {i + 1}",
            "command": lambda friend: self.show_friend_menu(friend)} for i in range(100)]
        
    def on_blocked_players(self, instance, value):
        # Load sample block list
        self.blocked_players.data = [{
            "text": f"Troublemaker {i + 1}",
            "command": lambda blocked_player: self.show_blocked_player_menu(blocked_player)
            } for i in range(100)]

    def show_friend_menu(self, friend):
        # Create the friend bubble if it doesn't exist yet
        if not hasattr(self, "friend_bubble"):
            self.friend_bubble = FriendBubble()

        # Set selected friend and bubble position
        self.friend_bubble.friend = friend
        self.friend_bubble.center_x = self.mouse_pos[0]
        self.friend_bubble.y = self.mouse_pos[1]

        # Show the widget if it isn't already visible
        if self.friend_bubble.parent is None:
            self.add_widget(self.friend_bubble)

    def show_blocked_player_menu(self, blocked_player):
        # Create the blocked player bubble if it doesn't exist yet
        if not hasattr(self, "blocked_player_bubble"):
            self.blocked_player_bubble = BlockedPlayerBubble()

        # Set selected blocked player and bubble position
        self.blocked_player_bubble.player = blocked_player
        self.blocked_player_bubble.center_x = self.mouse_pos[0]
        self.blocked_player_bubble.y = self.mouse_pos[1]

        # Show the widget if it isn't already visible
        if self.blocked_player_bubble.parent is None:
            self.add_widget(self.blocked_player_bubble)

    def message_friend(self, friend):
        print(f"Message '{friend.username}'")
        self.remove_widget(self.friend_bubble)

    def find_friend(self, friend):
        print(f"Find '{friend.username}'")
        self.remove_widget(self.friend_bubble)

    def remove_friend(self, friend):
        print(f"Remove '{friend.username}'")
        self.remove_widget(self.friend_bubble)

    def remove_blocked_player(self, blocked_player):
        print(f"Unblock '{blocked_player.text}'")
        self.remove_widget(self.blocked_player_bubble)


Builder.load_file("ui/dialogs/friends_dialog.kv")
