
package us.kbase.sampleservice;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: ReplaceSampleACLsParams</p>
 * <pre>
 * replace_sample_acls parameters.
 *         id - the ID of the sample to modify.
 *         acls - the ACLs to set on the sample.
 *         as_admin - replace the sample acls regardless of sample ACL contents as long as the user
 *             has full service administration permissions.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "id",
    "acls",
    "as_admin"
})
public class ReplaceSampleACLsParams {

    @JsonProperty("id")
    private String id;
    /**
     * <p>Original spec-file type: SampleACLs</p>
     * <pre>
     * Access control lists for a sample. Access levels include the privileges of the lower
     * access levels.
     * owner - the user that created and owns the sample.
     * admin - users that can administrate (e.g. alter ACLs) the sample.
     * write - users that can write (e.g. create a new version) to the sample.
     * read - users that can view the sample.
     * public_read - whether any user can read the sample, regardless of permissions.
     * </pre>
     * 
     */
    @JsonProperty("acls")
    private SampleACLs acls;
    @JsonProperty("as_admin")
    private Long asAdmin;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("id")
    public String getId() {
        return id;
    }

    @JsonProperty("id")
    public void setId(String id) {
        this.id = id;
    }

    public ReplaceSampleACLsParams withId(String id) {
        this.id = id;
        return this;
    }

    /**
     * <p>Original spec-file type: SampleACLs</p>
     * <pre>
     * Access control lists for a sample. Access levels include the privileges of the lower
     * access levels.
     * owner - the user that created and owns the sample.
     * admin - users that can administrate (e.g. alter ACLs) the sample.
     * write - users that can write (e.g. create a new version) to the sample.
     * read - users that can view the sample.
     * public_read - whether any user can read the sample, regardless of permissions.
     * </pre>
     * 
     */
    @JsonProperty("acls")
    public SampleACLs getAcls() {
        return acls;
    }

    /**
     * <p>Original spec-file type: SampleACLs</p>
     * <pre>
     * Access control lists for a sample. Access levels include the privileges of the lower
     * access levels.
     * owner - the user that created and owns the sample.
     * admin - users that can administrate (e.g. alter ACLs) the sample.
     * write - users that can write (e.g. create a new version) to the sample.
     * read - users that can view the sample.
     * public_read - whether any user can read the sample, regardless of permissions.
     * </pre>
     * 
     */
    @JsonProperty("acls")
    public void setAcls(SampleACLs acls) {
        this.acls = acls;
    }

    public ReplaceSampleACLsParams withAcls(SampleACLs acls) {
        this.acls = acls;
        return this;
    }

    @JsonProperty("as_admin")
    public Long getAsAdmin() {
        return asAdmin;
    }

    @JsonProperty("as_admin")
    public void setAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
    }

    public ReplaceSampleACLsParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("ReplaceSampleACLsParams"+" [id=")+ id)+", acls=")+ acls)+", asAdmin=")+ asAdmin)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
