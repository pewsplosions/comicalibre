# Comicalibre

### Install
Zip the contents of the src directory. Or download from the Releases, if anything is there.

Installing plugins in Calibre is as simple as opening Preferences > Plugins and clicking 'Load plugin from file' and choosing the zip file from above.

#### What is it?
Plugin that can be used to gather various metadata from Comic Vine and update Calibre's metadata to match.

#### Assumptions
This plugin, in its default state, assumes certain custom columns have been created in Calibre. For it to work properly these need to be there. (If you don't like the setup, see #Changes below.)

Note: The ampersand separated columns can be found by choosing comma separated and check the contains names box.

<u>Column List</u><br />
1. Characters with lookup characters - Ampersand separated text, shown in the Tag browser.
2. Creators with lookup creators - Ampersand separated text, shown in the Tag browser.
3. Story Arcs with lookup storyarcs - Ampersand separated text, shown in the Tag browser.
4. Physical Copy with lookup physicalcopy - Yes/No
5. Comic Vine Volume ID with lookup comicvinevolumeid - Integers
6. Comic Vine Issue ID with lookup comicvineissueid - Integers

#### How does it work?
Note: If the icon is not in your toolbar you may have to go to Preferences > Toolbars & menus > choose The Main Toolbar and add the Comicalibre icon to the right from the left.

It requires a Comic Vine API key to be entered. You can get this free from their site.

It can also take a comma separated list of tags. But this is optional.

Assuming the plugin finds metadata from Comic Vine, **it will completely replace anything that is already there.** This includes any tags entered above.

There are three buttons on the dialog. All ultimately do the same thing but they look for the needed information in different spots.

##### Title Processing
If the title option is chosen, it will parse the title string looking for specific data. The title string **MUST** be formatted a specific way for this to work.

```
Example: Title --- v1234 n0023
```

The plugin **REQUIRES** the triple dash. It will use it to parse the string to make 'Title' the book's title in calibre.

1234 **MUST** be the matching Comic Vine volume ID. This number would be the number in the Volume's main page's URL after the 4050- up to the next /

0023 is the issue number. This doesn't have to have leading 0s but it is usually easier to batch rename lots of files using them so the operating system file explorer keeps them in order when sorted by name.

###### When this is most useful
When you have lots of comic books from the same volume in a single folder.

There are lots of applications or explorer add-ons that can batch rename files. So in this case you would just need to rename them all at once with an increasing number.

For example in dolphin on kde if you have a new comic that has 78 issues named Imaginary. You could go to the volume page at Comic Vine and grab the volume ID. Then select all 78, right click and select rename. Then input something like: Imaginary --- v981023 n### and select to start at 001.

Then when you import all 78 of the above into calibre, it usually will not find any metadata so all it does is make the file name the book title.

Then you can just run Comicalibre on the 78 books and it will parse the title strings and get all the metadata for you.

##### Series Processing
If the series option is chose, it will look for the volume ID to be the series name. The issue number would then just be the series number.

Again, same as the title method, the series name **MUST** be exactly the volume ID on the Volumes Comic Vine URL after the 4050- part.

###### When this is most useful
If you've already imported all your books and do not have the title string correct, you cannot edit the title when you do a metadata edit on all selections at once.

You can of course just remove the books and re-add them if you have the files somewhere that you can easily rename. But if you already have series data input, you can use Calibre to rename the series to the volume ID from Comic Vine.

If the series is named the Volume ID and each book has the correct series ID (i.e. issue number) and the series processing option is chosen it will then replace all the metadata in the same way, including renaming the series back to the correct series name.

##### IDs Processing
A third option is to have two custom columns. comicvinevolumeid and comicvineissueid. Using this option will directly use those. The volume ID is the same as mentioned above. The issue ID in this case is a little different though. Instead of the issue number it is the Comic Vine ID for the issue. Just like finding the volume ID, you can find the issue ID by going to an issue page and looking at the URL. Instead of 4050 however it'd be 4000 that prefixes the issue ID.

###### When this is most useful
Comic Vine is essentially a wiki-like website. People can edit and add the data any time. So this option is mostly there to refresh metadata without having to rename the book.

When any of the options run successfully, it will fill the two custom columns along with the rest of the metadata. Inputting them manually would be a real hassle compared to the other two methods if you are trying to get your first run setup.

So assuming you've run the process on the books before. There really is no new setup to run this type of processing. Just select the books, open the dialog and click the button and it will run through and refresh the metadata on all of them. Assuming of course the Comic Vine IDs did not get altered at some point.

#### Changes
Comicalibre is not magic. It requires specific input data in order to get metadata from Comic Vine and puts the results into specific fields of the metadata for Calibre.

It doesn't do any kind of searching, matching, guessing, comparing, etc...

Frankly I just set things up I wanted them to be then automated the gathering in a way that works for me without much regard to what anyone else would want.

With that said, the reason I built this is because there really isn't a lot of options out there for automating comic book metadata with Calibre. So I thought I'd let anyone else use it that might want to as well.

**IF you don't like it...** I probably will not make changes for you. However, the code is not extremely difficult to understand and is somewhat separated into classes that do specific kinds of work. So if you really want to make some small changes, feel free to change the code for yourself.

For example, if you wanted to pull a field from comic vine that is not currently being pulled and put it into your own custom column. In the comicvine.py file there is a method that is creating the url params. You can just add to the fields it is asking for there. Then on the results section in the same file add the result of that new field to the metadata object in your custom column.

Another example would be if you want to make different columns for all the different types of creators instead of just having one column for all of them. Create the columns in Calibre. Edit the comicvine file again. You'll see where I'm already separating Authors. So you can just do that and make a new list for each type of creator. Add them to each of your columns on the results.

#### License
I don't really know anything about this, but all the examples I saw for calibre plugins used the GPL v3 license.

So that's what I threw in here as well.
