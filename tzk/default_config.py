# Default tzk config
# <<GENERATION_DETAILS>>

# This config file is live, unrestricted Python.
# You can add your own builders or logic here if necessary.
# tzk's package directory is on the PYTHONPATH when this module is imported,
# so if you want to import a function from, e.g., tzk.util,
# just say 'from tzk.util import whatever'.

#------------------------------------------------------------------------------#

# Imports. Don't remove this or you won't be able to configure builders.
from tzk import builders

# Name of the subfolder containing your wiki data and its tiddlywiki.info file.
wiki_folder = "wiki"


### COMMITTING ####
# Default commit message to use with 'tzk commit'.
# You can always use 'tzk commit -m' to use a different message on the fly.
commit_message = "daily checkpoint"

# Git remote to push changes to when you run 'tzk commit'.
commit_remote = "origin"

# Uncomment if you want to abort 'tzk commit' if you're not on a specific branch.
#commit_require_branch = "master"


### LISTENING ###
# Port to listen on. If you specify 8080 for example, you'll edit your wiki by going to
# http://localhost:8080 in your browser.
listen_port = 8080

# Uncomment if you want to require HTTP basic authentication when serving your wiki.
# **WARNING**: this is NOT secure for use over the open Internet or all but the
# simplest local networks, as the password is sent in the clear. For good
# security, you need to add a reverse proxy on top that secures the connection via SSL.
#listen_username = "my_user"
#listen_password = "my_password"


### BUILD ###
# Filter for tiddlers that should be included in a public export of the wiki.
_public_export_filt = r"""
    [is[system]]
    [tag[Public]]
    -[[$:/plugins/tiddlywiki/tiddlyweb]]
    -[[$:/plugins/tiddlywiki/filesystem]]
    -[prefix[$:/temp]]
    -[prefix[$:/state]]
    -[prefix[$:/sib/StorySaver/saved]]
    -[prefix[$:/sib/checkify/]]
    -[[$:/config/zettelkasten/Build/KillPhrases]]
"""

# Each "product" is a different deliverable or target. A product can be built
# by running 'tzk build PRODUCT'. You can include any number of products,
# each of which can use any number of "builders", micro-build steps that
# perform a small part of the build. The configured builders are run in sequence.
#
# See the "Builders" section of the tzk documentation
# for details on the available builders and their parameters.
#
# If you want to do something that's not covered by the existing builders,
# you can write your own, or you can run arbitrary shell commands
# using a 'builders.shell("my shell command here"),' builder.
products = {
    # The default configuration contains a single product for building a public wiki.
    'public': [
        builders.new_output_folder(),
        builders.export_public_tiddlers(_public_export_filt),
        builders.replace_private_people(),
        builders.set_tiddler_values({
            '$__config_sib_CurrentEditionPublicity.tid': 'public',
            '$__config_sib_IsPublicEdition.tid': 'false',
            '$__config_DefaultSidebarTab.tid': '$:/sib/SideBar/Explore',
            '$__DefaultTiddlers.tid': 'PublicHomepage',
            '$__config_PageControlButtons_Visibility_$__core_ui_Buttons_close-all.tid': 'show',
            '$__config_PageControlButtons_Visibility_$__core_ui_Buttons_control-panel.tid': 'hide',
            '$__config_PageControlButtons_Visibility_$__core_ui_Buttons_home.tid': 'show',
            '$__config_PageControlButtons_Visibility_$__core_ui_Buttons_more-page-actions.tid': 'show',
            '$__config_PageControlButtons_Visibility_$__core_ui_Buttons_new-tiddler.tid': 'hide',
            '$__config_PageControlButtons_Visibility_$__core_ui_Buttons_permaview.tid': 'show',
            '$__config_PageControlButtons_Visibility_$__core_ui_Buttons_tag-manager.tid': 'hide',
            '$__config_PageControlButtons_Visibility_$__sib_Buttons_NewSource.tid': 'hide',
            '$__config_PageControlButtons_Visibility_$__sib_Buttons_ReadingInbox.tid': 'hide',
            '$__config_ViewToolbarButtons_Visibility_$__core_ui_Buttons_close-others.tid': 'show',
            '$__config_ViewToolbarButtons_Visibility_$__core_ui_Buttons_edit.tid': 'hide',
            '$__config_ViewToolbarButtons_Visibility_$__core_ui_Buttons_info.tid': 'hide',
            '$__config_ViewToolbarButtons_Visibility_$__core_ui_Buttons_permalink.tid': 'show',
            '$__config_ViewToolbarButtons_Visibility_$__sib_Buttons_CopyPublicZettelkastenLink.tid': 'hide',
            '$__config_ViewToolbarButtons_Visibility_DoCopyTitleReference.tid': 'hide',
        }),
        builders.check_for_kill_phrases(),
        builders.save_attachments_externally(),
        builders.compile_html_file(externalize_attachments=True),
    ],
}
