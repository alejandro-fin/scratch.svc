import sys                                                                  as _sys

CODING_ROOT = "/home/alex/consultant1@CCL/dev"

MODULE_PATHS = [CODING_ROOT + "/scratch_fork/scratch.ops/src"]
import sys
sys.path.extend(MODULE_PATHS)

SCRATCH_ROOT_FORK            = CODING_ROOT + "/scratch_fork"
REMOTE_SCRATCH_FORK_ROOT     = 'https://alejandro-fin@github.com/alejandro-fin'
SCRATCH_LOCAL_REPOS          = ["scratch.svc"]

from conway.application.application                             import Application
from conway.util.command_parser                                 import CommandParser
from conway.util.dataframe_utils                                import DataFrameUtils
from conway.util.profiler                                       import Profiler
from conway.util.timestamp                                      import Timestamp

from conway_ops.onboarding.repo_bundle_subset                   import RepoBundleSubset
from conway_ops.repo_admin.branch_lifecycle_manager             import BranchLifecycleManager
from conway_ops.repo_admin.github_repo_inspector                import GitHub_RepoInspector
from conway_ops.repo_admin.repo_statics                         import RepoStatics
from conway_ops.repo_admin.repo_administration                  import RepoAdministration

from scratch_ops.onboarding.scratch_repo_bundle                 import ScratchRepoBundle

class Troubleshooter():

    def __init__(self):
        pass

    def run(self):
        '''
        '''                                           
        # Select what to troubleshoot, and comment out whatever we are not troubleshooting
        #
        with Profiler("Troubleshooting"):
            
            #self.create_pull_request()
            #self.troubleshoot_repo_report()
            self.troubleshoot_work_on_feature()

    def _init_SDCL_NB_Application(self):
        '''
        Helper method to initialize the Conway-based application that is used by notebooks, for when we need to 
        troubleshoot such notebooks
        '''
        SDLC_ROOT                           = "/home/alex/admin1@CCL/sdlc/"

        SDLC_MODULE_PATHS                   = [f"{SDLC_ROOT}/sdlc.ops/nb_apps"]
        sys.path.extend(SDLC_MODULE_PATHS)
        from sdlc_nb_application                                        import SDLC_NB_Application
        #SDLC_NB_Application()
        SDLC_NB_Application(profile_name="consultant1@CCL", project_name="scratch_fork")

    
    def create_pull_request(self):
        '''
        '''
        # Pre-flight: need to initialize an application since the GitHub_RepoInspector will  need to read an
        # application profile in order to get the GitHub token, among other things
        #
        self._init_SDCL_NB_Application()

        # Now the main troubleshooting
        REPO_NAME = 'scratch.svc'
        gh                                  = GitHub_RepoInspector(parent_url=REMOTE_SCRATCH_FORK_ROOT, repo_name=REPO_NAME)
        pr1                                 = gh.pull_request(from_branch   = "integration", 
                                                              to_branch     = "master", 
                                                              title         = "Dummy PR for test purposes",
                                                              body          = "Discard this PR")
        return pr1
        

    def troubleshoot_work_on_feature(self):
        '''
        '''
        # Pre-flight: need to initialize an application since the GitHub_RepoInspector will  need to read an
        # application profile in order to get the GitHub token, among other things
        #
        self._init_SDCL_NB_Application()

        PROFILE                             = Application.app().profile

        GH_ORGANIZATION                     = PROFILE["git"]["github_organization"]
        PROJECT                             = Application.app().project_under_profile
        REPO_LIST                           = PROFILE["projects"][PROJECT]
        LOCAL_DEV_ROOT                      = PROFILE["local_development"]["dev_root"]
        USER                                = PROFILE["git"]["user"]["name"]

        REMOTE_ROOT                         = f"https://{USER}@github.com/{GH_ORGANIZATION}"

        CRB                                 = ScratchRepoBundle()

        DEV_PROJECT_ROOT                    = f"{LOCAL_DEV_ROOT}/{PROJECT}"
        GB_SECRETS_PATH                     = Application.app().config.config_dict['secrets']['vault_location']
        PROJECT_LOCAL_BUNDLE       =         RepoBundleSubset(CRB, REPO_LIST)

        FEATURE_BRANCH                      = "afin-dev"

        dev_admin                           = BranchLifecycleManager(local_root         = DEV_PROJECT_ROOT, 
                                                                     remote_root        = REMOTE_ROOT, 
                                                                     repo_bundle        = PROJECT_LOCAL_BUNDLE,
                                                                     remote_gh_user     = USER, 
                                                                     gb_secrets_path    = GB_SECRETS_PATH)
        
        result                              = dev_admin.work_on_feature(FEATURE_BRANCH)
        return result

    def troubleshoot_repo_report(self):
        '''
        '''
        CRB                                 = ScratchRepoBundle()
        PUBLICATION_FOLDER                  = "C:/Alex/tmp2"
        
        conway_admin                        = RepoAdministration(local_root     = SCRATCH_ROOT_FORK, 
                                                                remote_root     = REMOTE_SCRATCH_FORK_ROOT, 
                                                                repo_bundle     = CRB)
        conway_admin.create_repo_report(publications_folder     = PUBLICATION_FOLDER, 
                                        repos_in_scope_l        = SCRATCH_LOCAL_REPOS)



        
if __name__ == "__main__":
    # execute only if run as a script
    def main(args):    
        troubleshooter                                              = Troubleshooter()    
        troubleshooter.run()

    main(_sys.argv)