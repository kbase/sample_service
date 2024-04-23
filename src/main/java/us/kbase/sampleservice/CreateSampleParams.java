
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
 * <p>Original spec-file type: CreateSampleParams</p>
 * <pre>
 * Parameters for creating a sample.
 * If Sample.id is null, a new Sample is created along with a new ID.
 * Otherwise, a new version of Sample.id is created. If Sample.id does not exist, an error
 *   is returned.
 * Any incoming user, version or timestamp in the incoming sample is ignored.
 * sample - the sample to save.
 * prior_version - if non-null, ensures that no other sample version is saved between
 *     prior_version and the version that is created by this save. If this is not the case,
 *     the sample will fail to save.
 * as_admin - run the method as a service administrator. The user must have full
 *     administration permissions.
 * as_user - create the sample as a different user. Ignored if as_admin is not true. Neither
 *     the administrator nor the impersonated user need have permissions to the sample if a
 *     new version is saved.
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "sample",
    "prior_version",
    "as_admin",
    "as_user"
})
public class CreateSampleParams {

    /**
     * <p>Original spec-file type: Sample</p>
     * <pre>
     * A Sample, consisting of a tree of subsamples and replicates.
     * id - the ID of the sample.
     * user - the user that saved the sample.
     * node_tree - the tree(s) of sample nodes in the sample. The the roots of all trees must
     *     be BioReplicate nodes. All the BioReplicate nodes must be at the start of the list,
     *     and all child nodes must occur after their parents in the list.
     * name - the name of the sample. Must be less than 255 characters.
     * save_date - the date the sample version was saved.
     * version - the version of the sample.
     * </pre>
     * 
     */
    @JsonProperty("sample")
    private Sample sample;
    @JsonProperty("prior_version")
    private Long priorVersion;
    @JsonProperty("as_admin")
    private Long asAdmin;
    @JsonProperty("as_user")
    private String asUser;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: Sample</p>
     * <pre>
     * A Sample, consisting of a tree of subsamples and replicates.
     * id - the ID of the sample.
     * user - the user that saved the sample.
     * node_tree - the tree(s) of sample nodes in the sample. The the roots of all trees must
     *     be BioReplicate nodes. All the BioReplicate nodes must be at the start of the list,
     *     and all child nodes must occur after their parents in the list.
     * name - the name of the sample. Must be less than 255 characters.
     * save_date - the date the sample version was saved.
     * version - the version of the sample.
     * </pre>
     * 
     */
    @JsonProperty("sample")
    public Sample getSample() {
        return sample;
    }

    /**
     * <p>Original spec-file type: Sample</p>
     * <pre>
     * A Sample, consisting of a tree of subsamples and replicates.
     * id - the ID of the sample.
     * user - the user that saved the sample.
     * node_tree - the tree(s) of sample nodes in the sample. The the roots of all trees must
     *     be BioReplicate nodes. All the BioReplicate nodes must be at the start of the list,
     *     and all child nodes must occur after their parents in the list.
     * name - the name of the sample. Must be less than 255 characters.
     * save_date - the date the sample version was saved.
     * version - the version of the sample.
     * </pre>
     * 
     */
    @JsonProperty("sample")
    public void setSample(Sample sample) {
        this.sample = sample;
    }

    public CreateSampleParams withSample(Sample sample) {
        this.sample = sample;
        return this;
    }

    @JsonProperty("prior_version")
    public Long getPriorVersion() {
        return priorVersion;
    }

    @JsonProperty("prior_version")
    public void setPriorVersion(Long priorVersion) {
        this.priorVersion = priorVersion;
    }

    public CreateSampleParams withPriorVersion(Long priorVersion) {
        this.priorVersion = priorVersion;
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

    public CreateSampleParams withAsAdmin(Long asAdmin) {
        this.asAdmin = asAdmin;
        return this;
    }

    @JsonProperty("as_user")
    public String getAsUser() {
        return asUser;
    }

    @JsonProperty("as_user")
    public void setAsUser(String asUser) {
        this.asUser = asUser;
    }

    public CreateSampleParams withAsUser(String asUser) {
        this.asUser = asUser;
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
        return ((((((((((("CreateSampleParams"+" [sample=")+ sample)+", priorVersion=")+ priorVersion)+", asAdmin=")+ asAdmin)+", asUser=")+ asUser)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
